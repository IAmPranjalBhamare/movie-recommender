# 🎬 Movie Recommender System

A modern, full-stack machine learning application that recommends movies based on content similarity. Built with Python, Flask, and a beautiful responsive web interface.

## ✨ Features

- **🔍 Intelligent Search** - Autocomplete movie search with posters and ratings
- **🎯 Smart Recommendations** - Content-based recommendations using TF-IDF and cosine similarity
- **🎨 Beautiful UI** - Responsive design with movie posters, cast, directors, and ratings
- **⚡ High Performance** - Deployed on Render with optimized memory usage
- **📊 4,806 Movies** - Complete TMDB dataset with detailed metadata

## 🚀 Live Demo

**Website:** [https://movie-recommender-system-4-nds8.onrender.com](https://movie-recommender-system-4-nds8.onrender.com)

### Features:
- Search for any movie with autocomplete suggestions
- View detailed movie information (poster, rating, cast, director, genres, overview)
- Get personalized movie recommendations
- Browse popular movies from the sidebar

## 📋 How It Works

### Algorithm
The system uses **Content-Based Filtering**:
1. **Feature Extraction** - Combines overview, genres, keywords, cast, and crew
2. **Text Processing** - Applies stemming and TF-IDF vectorization
3. **Similarity Calculation** - Uses cosine similarity to find similar movies
4. **Ranking** - Returns top-N most similar movies

### Data Pipeline
- **Input:** TMDB 5000 Movies Dataset (4,806 movies)
- **Processing:** Text cleaning, feature extraction, stemming
- **Models:** Sparse TF-IDF vectorizer, cosine similarity matrix
- **Output:** Movie metadata and similarity scores

## 🛠️ Tech Stack

### Backend
- **Framework:** Flask
- **ML Libraries:** scikit-learn, NLTK, pandas, numpy
- **Server:** Gunicorn
- **Deployment:** Docker, Render.com

### Frontend
- **HTML5 / CSS3 / JavaScript**
- **Bootstrap 5** - Responsive design
- **Font Awesome** - Icons
- **TMDB API** - Movie posters and metadata

### Data
- **Source:** TMDB 5000 Movies Dataset
- **Size:** 4,806 movies with metadata

## 📦 Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/IAmPranjalBhamare/movie-recommender-system.git
   cd movie-recommender-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate models** (builds similarity matrix and metadata)
   ```bash
   python generate_models.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

   Visit `http://localhost:5000` in your browser

## 🐳 Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t movie-recommender .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 movie-recommender
   ```

3. **Access the application**
   - Open `http://localhost:5000` in your browser

## 📁 Project Structure

```
movie-recommender-system/
├── app.py                      # Flask API server
├── index.html                  # Frontend UI
├── generate_models.py          # Model generation script
├── gunicorn_config.py         # Gunicorn configuration
├── Dockerfile                  # Docker configuration
├── requirements.txt            # Python dependencies
├── tmdb_5000_movies.csv       # Movie metadata
├── tmdb_5000_credits.csv      # Cast and crew data
├── movie_dict.pkl             # Title-to-index mapping
├── similarity.pkl             # Cosine similarity matrix
├── movie_metadata.pkl         # Full movie details
└── README.md                  # This file
```

## 🔌 API Endpoints

### GET `/`
Returns the web UI interface.

### GET `/health`
Health check endpoint.
```
Response: {"status": "healthy", "service": "Movie Recommender API"}
```

### POST `/recommend`
Get movie recommendations.
```json
Request:
{
  "movie": "Avatar",
  "num_recommendations": 5
}

Response:
{
  "movie": "Avatar",
  "recommendations": ["Movie 1", "Movie 2", "Movie 3", "Movie 4", "Movie 5"]
}
```

### GET `/movies?page=1&limit=10`
Get paginated list of movies.
```json
Response:
{
  "total": 4806,
  "page": 1,
  "limit": 10,
  "movies": ["Movie 1", "Movie 2", ...]
}
```

### GET `/movie/<movie_name>`
Get detailed information about a specific movie.
```json
Response:
{
  "title": "Avatar",
  "overview": "...",
  "poster_path": "/path/to/poster.jpg",
  "vote_average": 7.2,
  "release_date": "2009-12-18",
  "genres": ["Action", "Adventure", "Sci-Fi"],
  "cast": ["Sam Worthington", "Zoe Saldana", ...],
  "crew": ["James Cameron"]
}
```

### GET `/search?q=avatar&limit=10`
Search movies with autocomplete.
```json
Response:
{
  "results": [
    {
      "title": "Avatar",
      "poster_path": "/path/to/poster.jpg",
      "vote_average": 7.2,
      "genres": ["Action", "Adventure"]
    },
    ...
  ]
}
```

## 🎯 Usage Examples

### Using the Web UI
1. Visit the website
2. Search for a movie in the search bar (e.g., "Avatar")
3. View movie details with poster, cast, and director
4. Check recommendations below the movie card
5. Click any recommendation to explore further

### Using curl/PowerShell
```bash
# Get recommendations for Avatar
curl -X POST https://movie-recommender-system-4-nds8.onrender.com/recommend \
  -H "Content-Type: application/json" \
  -d '{"movie":"Avatar","num_recommendations":5}'

# Search for movies
curl "https://movie-recommender-system-4-nds8.onrender.com/search?q=inception"

# Get movie details
curl "https://movie-recommender-system-4-nds8.onrender.com/movie/Avatar"
```

### Using Python
```python
import requests

# Get recommendations
response = requests.post(
    'https://movie-recommender-system-4-nds8.onrender.com/recommend',
    json={'movie': 'Avatar', 'num_recommendations': 5}
)
print(response.json())
```

## 🔧 Configuration

### Memory Optimization
- **Gunicorn workers:** 1 (optimized for 512MB memory)
- **App preloading:** Enabled (models loaded once, shared by workers)
- **Max requests:** 1000 (prevents memory leaks)

### Performance
- Model generation: ~15 seconds (on first build)
- API response time: <100ms for recommendations
- Search response time: <50ms for autocomplete

## 🚢 Deployment

### Deploy to Render.com (Recommended)

1. Push to GitHub
   ```bash
   git push origin main
   ```

2. Create new Web Service on Render
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt && python generate_models.py`
   - Set start command: `gunicorn --config gunicorn_config.py app:app`
   - Allocate minimum 512MB RAM

3. Your app will be live in 2-5 minutes

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| Total Movies | 4,806 |
| API Response Time | <100ms |
| Search Time | <50ms |
| Memory Usage | ~120MB |
| Recommendation Accuracy | Content-based similarity |

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit (`git commit -m 'Add amazing feature'`)
5. Push (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 🐛 Known Issues & Limitations

- Movie search is case-insensitive for better UX
- Recommendations are based on content similarity only (no collaborative filtering)
- Free tier deployment has cold start delays (~50 seconds)
- Poster images depend on TMDB API availability

## 📊 Dataset

**Source:** TMDB 5000 Movies Dataset
- 4,806 movies with complete metadata
- Features: genres, keywords, cast, crew, budget, revenue, ratings
- Time period: 1916-2016

## 🔐 Security

- CORS enabled for cross-origin requests
- Input validation on all endpoints
- No sensitive data stored or logged
- HTTPS enforced in production

## 📝 License

MIT License - see the LICENSE file for details

## 🙏 Acknowledgments

- **TMDB** for the comprehensive movie dataset
- **scikit-learn** for ML tools
- **Flask** for the web framework
- **Bootstrap** for the UI framework
- **Render** for hosting

## 📞 Contact & Support

- **GitHub Issues:** Report bugs or request features
- **Live Demo:** [Visit the website](https://movie-recommender-system-4-nds8.onrender.com)

---

**Made with ❤️ by Pranjal Bhamare**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-2.0-green)
![ML](https://img.shields.io/badge/ML-scikit%2Dlearn-orange)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Authors

- Your Name - Initial work

## Acknowledgments

- TMDB for the movie dataset
- Scikit-learn for similarity metrics
- Flask for the API framework
