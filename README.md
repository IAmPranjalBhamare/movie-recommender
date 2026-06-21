# Movie Recommender System

A machine learning-based movie recommendation system that uses content-based filtering to suggest movies based on genres, keywords, cast, crew, and overview information.

## Features

- **Content-Based Filtering**: Recommends movies based on similarity metrics
- **REST API**: Flask-based API for easy integration
- **Containerized Deployment**: Docker support for consistent deployment
- **AWS Deployment Ready**: CI/CD pipeline configured for automated deployment to AWS

## Project Structure

```
movie-recommender-system/
├── movie-recommender-system.ipynb  # Main notebook with ML model
├── app.py                           # Flask API application
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Container configuration
├── tmdb_5000_movies.csv            # Movie dataset
├── tmdb_5000_credits.csv           # Credits dataset
├── movies.pkl                       # Pre-trained model data
├── similarity.pkl                   # Similarity matrix
├── movie_dict.pkl                   # Movie dictionary
└── .github/workflows/deploy.yml    # CI/CD pipeline
```

## Installation

### Local Development

1. Clone the repository:

```bash
git clone https://github.com/your-username/movie-recommender-system.git
cd movie-recommender-system
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Flask app:

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Docker Deployment

1. Build the Docker image:

```bash
docker build -t movie-recommender-system .
```

2. Run the container:

```bash
docker run -p 5000:5000 movie-recommender-system
```

## API Endpoints

### Health Check

```
GET /health
Response: { "status": "healthy", "service": "Movie Recommender API" }
```

### Get Recommendations

```
POST /recommend
Request Body: {
  "movie": "Movie Title",
  "num_recommendations": 5
}
Response: {
  "movie": "Movie Title",
  "recommendations": ["Movie 1", "Movie 2", ...]
}
```

### Get Movies List

```
GET /movies?page=1&limit=10
Response: {
  "total": 4809,
  "page": 1,
  "limit": 10,
  "movies": ["Movie 1", "Movie 2", ...]
}
```

### API Info

```
GET /
Response: {
  "message": "Movie Recommender System API",
  "version": "1.0.0",
  "endpoints": {...}
}
```

## Example Usage

### Using cURL

```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"movie": "The Avengers", "num_recommendations": 5}'
```

### Using Python

```python
import requests

url = "http://localhost:5000/recommend"
data = {"movie": "The Avengers", "num_recommendations": 5}
response = requests.post(url, json=data)
print(response.json())
```

## Deployment to AWS

### Prerequisites

1. AWS Account with ECR, ECS, and IAM permissions
2. GitHub repository with this code
3. AWS credentials configured

### Setup Steps

1. Create an ECR repository:

```bash
aws ecr create-repository --repository-name movie-recommender-system --region us-east-1
```

2. Create an ECS cluster and service (or update existing ones)

3. Add GitHub Secrets to your repository:
   - `AWS_ROLE_TO_ASSUME`: AWS IAM role ARN for OIDC
   - `AWS_ECS_CLUSTER`: ECS cluster name
   - `AWS_ECS_SERVICE`: ECS service name

4. Push to main branch:

```bash
git push origin main
```

The GitHub Actions workflow will automatically build and deploy your application.

## Model Information

The recommendation system uses:

- **Algorithm**: Cosine Similarity
- **Features**: Genres, Keywords, Cast, Crew, Overview
- **Dataset**: TMDB 5000 Movies
- **Total Movies**: ~4,800

## Performance

- Average recommendation time: < 100ms
- Container memory usage: ~500MB
- Support for ~100 concurrent requests

## Future Enhancements

- [ ] Collaborative filtering
- [ ] Hybrid recommendation engine
- [ ] User rating system
- [ ] Watchlist functionality
- [ ] Advanced filtering options
- [ ] GraphQL API support

## License

MIT License - see LICENSE file for details

## Contributing

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
