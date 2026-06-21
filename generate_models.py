"""
Generate model files (similarity matrix and movie dictionary) from CSV data.
This script runs during Docker build to create .pkl files needed for the API.
"""

import pandas as pd
import numpy as np
import ast
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import nltk

print("📦 Generating recommendation model...")

# Download required NLTK data
nltk.download('punkt', quiet=True)

# Load data
print("📖 Loading data...")
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

# Merge datasets
print("🔗 Merging datasets...")
movies = movies.merge(credits, on='title')

# Select features
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# Clean data
print("🧹 Cleaning data...")
movies.dropna(inplace=True)

# Convert functions
def convert(obj):
    """Extract names from JSON-like string"""
    L = []
    try:
        for i in ast.literal_eval(obj):
            L.append(i['name'])
    except:
        pass
    return L

def convert3(obj):
    """Extract first 3 actors"""
    L = []
    cnt = 0
    try:
        for i in ast.literal_eval(obj):
            if cnt != 3:
                L.append(i['name'])
                cnt += 1
            else:
                break
    except:
        pass
    return L

def fetch_director(obj):
    """Extract director name"""
    L = []
    try:
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                L.append(i['name'])
                break
    except:
        pass
    return L

# Apply conversions
print("🎬 Processing genres, keywords, cast, crew...")
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert3)
movies['crew'] = movies['crew'].apply(fetch_director)

# Process overview
print("📝 Processing overview...")
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# Remove spaces from names
print("✨ Cleaning names...")
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

# Combine features
print("🔀 Combining features...")
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# Create dataframe with tags
new_df = movies[['movie_id', 'title', 'tags']]
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

# Apply stemming
print("🌱 Applying stemming...")
ps = PorterStemmer()

def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

# Vectorization
print("🔢 Vectorizing text...")
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# Calculate similarity
print("📊 Calculating similarity matrix...")
similarity = cosine_similarity(vectors)

# Save models
print("💾 Saving models...")
pickle.dump(new_df.to_dict(), open('movie_dict.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))
pickle.dump(new_df[['movie_id', 'title']].to_dict(), open('movies.pkl', 'wb'))

print("✅ Models generated successfully!")
print(f"   - Total movies: {len(new_df)}")
print(f"   - Features extracted: {vectors.shape[1]}")
