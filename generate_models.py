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

# Select features (only columns that exist in the dataset)
available_columns = ['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']
# Add optional columns if they exist
for col in ['vote_average', 'poster_path', 'release_date']:
    if col in movies.columns:
        available_columns.append(col)

movies = movies[available_columns]

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

# Save original metadata before cleaning for display purposes
print("📸 Preparing metadata...")
metadata_dict = {}
for idx, row in movies.iterrows():
    # Safely get optional columns
    poster = row['poster_path'] if 'poster_path' in movies.columns and pd.notna(row['poster_path']) else None
    rating = float(row['vote_average']) if 'vote_average' in movies.columns and pd.notna(row['vote_average']) else 0
    release = str(row['release_date']).split()[0] if 'release_date' in movies.columns and pd.notna(row['release_date']) else 'N/A'
    
    metadata_dict[row['title'].lower()] = {
        'title': row['title'],
        'overview': row['overview'],
        'poster_path': poster,
        'vote_average': rating,
        'release_date': release,
        'genres': row['genres'],
        'cast': row['cast'],
        'crew': row['crew'],
    }

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
new_df = movies[['movie_id', 'title', 'tags']].copy()
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
vectors = cv.fit_transform(new_df['tags'])  # Keep as sparse matrix

# Calculate similarity
print("📊 Calculating similarity matrix...")
similarity = cosine_similarity(vectors)  # Returns sparse matrix

# Save models
print("💾 Saving models...")
# Create title-to-index mapping (case-insensitive)
title_to_index = {title.lower(): idx for idx, title in enumerate(new_df['title'].values)}
pickle.dump(title_to_index, open('movie_dict.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))  # Sparse matrix
pickle.dump(metadata_dict, open('movie_metadata.pkl', 'wb'))  # Movie metadata with poster, cast, etc
pickle.dump(new_df[['movie_id', 'title']].values, open('movies.pkl', 'wb'))  # Lightweight array

print("✅ Models generated successfully!")
print(f"   - Total movies: {len(new_df)}")
print(f"   - Features extracted: {vectors.shape[1]}")
