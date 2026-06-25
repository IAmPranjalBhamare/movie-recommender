# 🎬 Movie Recommender System

A machine learning-based web application that recommends movies based on content similarity. Built entirely with Python and Streamlit, and deployed seamlessly to the web.

## 🚀 Live Demo

**Check out the live website here:** [https://movie-recommender-9ijk.onrender.com/](https://movie-recommender-9ijk.onrender.com/)

---

## ✨ Features

- **🔍 Intelligent Search** - Select or type a movie from the interactive dropdown.
- **🎯 Smart Recommendations** - Suggests the top 5 most similar movies based on the selected title.
- **🧠 Machine Learning** - Uses Content-Based Filtering (Cosine Similarity and TF-IDF/Count Vectorization) to calculate movie similarities.
- **🎨 Clean UI** - A highly responsive, minimal user interface powered by Streamlit.

---

## 🛠️ Tech Stack

- **Frontend & Backend:** [Streamlit](https://streamlit.io/)
- **Machine Learning:** Scikit-Learn, Pandas, NumPy
- **Data Source:** TMDB 5000 Movies Dataset
- **Deployment:** [Render](https://render.com/) (with Git Large File Storage for models)

---

## 📋 How It Works

1. **Data Processing:** The system processes movie metadata (like genres, keywords, cast, and crew) from the TMDB dataset.
2. **Vectorization:** Text data is converted into numeric vectors.
3. **Similarity Matrix:** Cosine similarity is calculated to find the mathematical distance between different movies.
4. **Recommendation:** When a user selects a movie, the app sorts the similarity matrix and fetches the 5 closest matches.

---

## 💻 How to Run Locally

If you want to run this project on your own computer, follow these steps:

**1. Clone the repository**

```bash
git clone https://github.com/IAmPranjalBhamare/movie-recommender.git
cd movie-recommender
```
