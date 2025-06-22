import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler



text_col = 'overview'
numeric_cols = ['popularity', 'vote_average', 'vote_count', 'release_date']
genre_cols = ['Adventure', 'Fantasy', 'Animation', 'Drama', 'Horror', 'Action', 'Comedy', 'History',
              'Western', 'Thriller', 'Crime', 'Documentary', 'Science Fiction', 'Mystery', 'Music',
              'Romance', 'Family', 'War', 'TV Movie']

# # Normalize numeric columns to [0,1] scale for better combination
# scaler = MinMaxScaler()
# numeric_scaled = scaler.fit_transform(df[numeric_cols])

# TF-IDF for overview text
tfidf = TfidfVectorizer(stop_words='english', max_features=300)
overview_tfidf = tfidf.fit_transform(df[text_col]).toarray()

# Weight genres higher to emphasize genre similarity
genre_weight = 5  # increased weight for genres
weighted_genres = df[genre_cols].values * genre_weight
numeric_=df[numeric_cols]

# Combine all features (weighted genres, text, normalized numeric)
combined_features = np.hstack([
    overview_tfidf,
    weighted_genres,
    numeric_
])

def recommend_movies_advanced_unscaled(movie_title, df_scaled, df_original, combined_features, genre_cols, top_n=5, min_genre_overlap=1):
    # Find movie index in scaled df
    matches = df_scaled[df_scaled['title'].str.lower() == movie_title.lower()]
    if matches.empty:
        return f"No movie found with title: '{movie_title}'"
    idx = matches.index[0]

    # Genre filtering
    input_genres = df_scaled.loc[idx, genre_cols].values
    genre_overlap = (df_scaled[genre_cols].values * input_genres).sum(axis=1)
    candidate_mask = genre_overlap >= min_genre_overlap
    candidate_indices = np.where(candidate_mask)[0]

    # Similarity calculation limited to genre-similar candidates
    candidate_features = combined_features[candidate_indices]
    input_feature = combined_features[idx].reshape(1, -1)
    similarity_scores = cosine_similarity(input_feature, candidate_features).flatten()

    # Sort and select top_n excluding the input movie itself
    sorted_indices = similarity_scores.argsort()[::-1]
    sorted_indices = sorted_indices[1:top_n+1]
    recommended_indices = candidate_indices[sorted_indices]

    # Use original unscaled df for numeric columns display
    recommendations = df_original.iloc[recommended_indices][['title', 'popularity', 'vote_average', 'overview']].copy()
    recommendations.reset_index(drop=True, inplace=True)
    recommendations.index += 1

    # Truncate overview text for display
    recommendations['overview'] = recommendations['overview'].apply(lambda x: x[:150] + '...' if isinstance(x, str) and len(x) > 150 else x)

    return recommendations

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler



text_col = 'overview'
numeric_cols = ['popularity', 'vote_average', 'vote_count', 'release_date']
genre_cols = ['Adventure', 'Fantasy', 'Animation', 'Drama', 'Horror', 'Action', 'Comedy', 'History',
              'Western', 'Thriller', 'Crime', 'Documentary', 'Science Fiction', 'Mystery', 'Music',
              'Romance', 'Family', 'War', 'TV Movie']

# # Normalize numeric columns to [0,1] scale for better combination
# scaler = MinMaxScaler()
# numeric_scaled = scaler.fit_transform(df[numeric_cols])

# TF-IDF for overview text
tfidf = TfidfVectorizer(stop_words='english', max_features=300)
overview_tfidf = tfidf.fit_transform(df[text_col]).toarray()

# Weight genres higher to emphasize genre similarity
genre_weight = 5  # increased weight for genres
weighted_genres = df[genre_cols].values * genre_weight
numeric_=df[numeric_cols]

# Combine all features (weighted genres, text, normalized numeric)
combined_features = np.hstack([
    overview_tfidf,
    weighted_genres,
    numeric_
])

def recommend_movies_advanced_unscaled(movie_title, df_scaled, df_original, combined_features, genre_cols, top_n=5, min_genre_overlap=1):
    # Find movie index in scaled df
    matches = df_scaled[df_scaled['title'].str.lower() == movie_title.lower()]
    if matches.empty:
        return f"No movie found with title: '{movie_title}'"
    idx = matches.index[0]

    # Genre filtering
    input_genres = df_scaled.loc[idx, genre_cols].values
    genre_overlap = (df_scaled[genre_cols].values * input_genres).sum(axis=1)
    candidate_mask = genre_overlap >= min_genre_overlap
    candidate_indices = np.where(candidate_mask)[0]

    # Similarity calculation limited to genre-similar candidates
    candidate_features = combined_features[candidate_indices]
    input_feature = combined_features[idx].reshape(1, -1)
    similarity_scores = cosine_similarity(input_feature, candidate_features).flatten()

    # Sort and select top_n excluding the input movie itself
    sorted_indices = similarity_scores.argsort()[::-1]
    sorted_indices = sorted_indices[1:top_n+1]
    recommended_indices = candidate_indices[sorted_indices]

    # Use original unscaled df for numeric columns display
    recommendations = df_original.iloc[recommended_indices][['title', 'popularity', 'vote_average', 'overview']].copy()
    recommendations.reset_index(drop=True, inplace=True)
    recommendations.index += 1

    # Truncate overview text for display
    recommendations['overview'] = recommendations['overview'].apply(lambda x: x[:150] + '...' if isinstance(x, str) and len(x) > 150 else x)

    return recommendations


import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler



text_col = 'overview'
numeric_cols = ['popularity', 'vote_average', 'vote_count', 'release_date']
genre_cols = ['Adventure', 'Fantasy', 'Animation', 'Drama', 'Horror', 'Action', 'Comedy', 'History',
              'Western', 'Thriller', 'Crime', 'Documentary', 'Science Fiction', 'Mystery', 'Music',
              'Romance', 'Family', 'War', 'TV Movie']

# # Normalize numeric columns to [0,1] scale for better combination
# scaler = MinMaxScaler()
# numeric_scaled = scaler.fit_transform(df[numeric_cols])

# TF-IDF for overview text
tfidf = TfidfVectorizer(stop_words='english', max_features=300)
overview_tfidf = tfidf.fit_transform(df[text_col]).toarray()

# Weight genres higher to emphasize genre similarity
genre_weight = 5  # increased weight for genres
weighted_genres = df[genre_cols].values * genre_weight
numeric_=df[numeric_cols]

# Combine all features (weighted genres, text, normalized numeric)
combined_features = np.hstack([
    overview_tfidf,
    weighted_genres,
    numeric_
])

def recommend_movies_advanced_unscaled(movie_title, df_scaled, df_original, combined_features, genre_cols, top_n=5, min_genre_overlap=1):
    # Find movie index in scaled df
    matches = df_scaled[df_scaled['title'].str.lower() == movie_title.lower()]
    if matches.empty:
        return f"No movie found with title: '{movie_title}'"
    idx = matches.index[0]

    # Genre filtering
    input_genres = df_scaled.loc[idx, genre_cols].values
    genre_overlap = (df_scaled[genre_cols].values * input_genres).sum(axis=1)
    candidate_mask = genre_overlap >= min_genre_overlap
    candidate_indices = np.where(candidate_mask)[0]

    # Similarity calculation limited to genre-similar candidates
    candidate_features = combined_features[candidate_indices]
    input_feature = combined_features[idx].reshape(1, -1)
    similarity_scores = cosine_similarity(input_feature, candidate_features).flatten()

    # Sort and select top_n excluding the input movie itself
    sorted_indices = similarity_scores.argsort()[::-1]
    sorted_indices = sorted_indices[1:top_n+1]
    recommended_indices = candidate_indices[sorted_indices]

    # Use original unscaled df for numeric columns display
    recommendations = df_original.iloc[recommended_indices][['title', 'popularity', 'vote_average', 'overview']].copy()
    recommendations.reset_index(drop=True, inplace=True)
    recommendations.index += 1

    # Truncate overview text for display
    recommendations['overview'] = recommendations['overview'].apply(lambda x: x[:150] + '...' if isinstance(x, str) and len(x) > 150 else x)

    return recommendations



