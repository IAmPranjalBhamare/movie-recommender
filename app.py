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
    with open('movie_metadata.pkl', 'rb') as f:
        movie_metadata = pickle.load(f)  # metadata dict with poster, cast, etc
    
    # title-to-index mapping (already case-insensitive from generation)
    title_to_idx = movie_dict
    print(f"Models loaded successfully! ({len(movies_data)} movies)")
    print(f"Sample movies: {list(title_to_idx.keys())[:5]}")
except Exception as e:
    print(f"Error loading models: {e}")
    movies_data = None
    similarity = None
    title_to_idx = {}
    movie_metadata = {}

def recommend(movie_name, num_recommendations=5):
    """
    Recommend movies based on similarity (with metadata)
    """
    movie_name_lower = movie_name.lower().strip()
    
    if movie_name_lower not in title_to_idx:
        # Try to find partial matches
        partial_matches = [m for m in title_to_idx.keys() if movie_name_lower in m]
        if partial_matches:
            return {"error": f"Movie '{movie_name}' not found. Did you mean: {', '.join(partial_matches[:3])}?"}
        return {"error": f"Movie '{movie_name}' not found in database. Please check the spelling."}
    
    movie_index = title_to_idx[movie_name_lower]
    distances = similarity[movie_index].toarray().flatten() if hasattr(similarity[movie_index], 'toarray') else similarity[movie_index]
    
    # Get top similar movies (excluding the movie itself at index 0)
    sorted_indices = np.argsort(distances)[::-1][1:num_recommendations+1]
    
    recommendations = []
    for idx in sorted_indices:
        rec_title = str(movies_data[idx][1])
        rec_title_lower = rec_title.lower()
        
        # Get metadata if available
        if rec_title_lower in movie_metadata:
            meta = movie_metadata[rec_title_lower]
            recommendations.append({
                "title": rec_title,
                "poster_path": meta.get("poster_path"),
                "vote_average": meta.get("vote_average", 0),
                "genres": meta.get("genres", [])
            })
        else:
            recommendations.append({
                "title": rec_title,
                "poster_path": None,
                "vote_average": 0,
                "genres": []
            })
    
    return {"movie": movies_data[movie_index][1], "recommendations": recommendations}

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
        search = request.args.get('search', '', type=str).lower()
        
        if limit > 100:
            limit = 100
        
        # Get all movies
        movies_list = [str(m[1]) for m in movies_data]
        
        # Filter by search if provided
        if search:
            movies_list = [m for m in movies_list if search in m.lower()]
        
        total = len(movies_list)
        start = (page - 1) * limit
        end = start + limit
        paginated_movies = movies_list[start:end]
        
        return jsonify({
            "total": total,
            "page": page,
            "limit": limit,
            "movies": paginated_movies
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/movie/<movie_name>', methods=['GET'])
def get_movie_details(movie_name):
    """Get detailed information about a specific movie"""
    try:
        movie_name_lower = movie_name.lower().strip()
        
        if movie_name_lower not in movie_metadata:
            return jsonify({"error": f"Movie '{movie_name}' not found"}), 404
        
        metadata = movie_metadata[movie_name_lower]
        return jsonify(metadata), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search', methods=['GET'])
def search_movies():
    """Search for movies with autocomplete"""
    try:
        query = request.args.get('q', '', type=str).lower().strip()
        limit = request.args.get('limit', 10, type=int)
        
        if not query or len(query) < 2:
            return jsonify({"results": []}), 200
        
        # Find matching movies
        matches = [title for title in title_to_idx.keys() if query in title][:limit]
        
        results = []
        for title in matches:
            if title in movie_metadata:
                meta = movie_metadata[title]
                results.append({
                    'title': meta['title'],
                    'poster_path': meta.get('poster_path'),
                    'vote_average': meta.get('vote_average', 0),
                    'genres': meta.get('genres', [])
                })
        
        return jsonify({"results": results}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
