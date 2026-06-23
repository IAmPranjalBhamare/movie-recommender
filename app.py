import pickle
import numpy as np
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Load pre-trained models and data
try:
    with open('movies.pkl', 'rb') as f:
        movies_data = pickle.load(f)  # numpy array of [movie_id, title] pairs
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)  # sparse matrix
    with open('movie_dict.pkl', 'rb') as f:
        movie_dict = pickle.load(f)  # {'title': {movie_title: index, ...}}
    
    # Extract title-to-index mapping
    title_to_idx = movie_dict.get('title', {})
    print(f"Models loaded successfully! ({len(movies_data)} movies)")
except Exception as e:
    print(f"Error loading models: {e}")
    movies_data = None
    similarity = None
    title_to_idx = {}

def recommend(movie_name, num_recommendations=5):
    """
    Recommend movies based on similarity
    """
    if movie_name not in title_to_idx:
        return {"error": f"Movie '{movie_name}' not found in database"}
    
    movie_index = title_to_idx[movie_name]
    distances = similarity[movie_index].toarray().flatten() if hasattr(similarity[movie_index], 'toarray') else similarity[movie_index]
    
    # Get top similar movies (excluding the movie itself at index 0)
    sorted_indices = np.argsort(distances)[::-1][1:num_recommendations+1]
    
    recommendations = []
    for idx in sorted_indices:
        recommendations.append(str(movies_data[idx][1]))
    
    return {"movie": movie_name, "recommendations": recommendations}

@app.route('/', methods=['GET'])
def home():
    """Serve the web UI"""
    try:
        return send_file('index.html')
    except:
        # Fallback to JSON API info
        return jsonify({
            "message": "Movie Recommender System API",
            "version": "1.0.0",
            "endpoints": {
                "/recommend": "POST - Get movie recommendations",
                "/health": "GET - Check API health"
            }
        })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "Movie Recommender API"})

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    try:
        data = request.get_json()
        movie_name = data.get('movie', '').strip()
        num_recommendations = data.get('num_recommendations', 5)
        
        if not movie_name:
            return jsonify({"error": "Movie name is required"}), 400
        
        if not isinstance(num_recommendations, int) or num_recommendations < 1:
            num_recommendations = 5
        
        result = recommend(movie_name, num_recommendations)
        
        if "error" in result:
            return jsonify(result), 404
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/movies', methods=['GET'])
def get_movies():
    """
    Get available movies (paginated)
    """
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        if limit > 100:
            limit = 100
        
        start = (page - 1) * limit
        end = start + limit
        
        movies_list = [str(m[1]) for m in movies_data]  # Extract titles from numpy array
        total = len(movies_list)
        paginated_movies = movies_list[start:end]
        
        return jsonify({
            "total": total,
            "page": page,
            "limit": limit,
            "movies": paginated_movies
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
