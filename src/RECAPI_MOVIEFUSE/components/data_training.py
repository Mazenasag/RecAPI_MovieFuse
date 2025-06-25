import os
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from RECAPI_MOVIEFUSE.entity.config_entity import ModelTrainingConfig


class MovieRecommender:
    def __init__(self, config: ModelTrainingConfig):
        self.config = config
        self.df_original = self.config.df_original
        self.model = SentenceTransformer(config.model_name)

    def preprocess_and_cache(self):
        combined_path = self.config.combined_path
        df_scaled_path = self.config.df_original

        if os.path.exists(combined_path) and os.path.exists(df_scaled_path):
            print("\n✅ Loading precomputed features...")
            self.combined_features = np.load(combined_path)
            self.df_scaled = pd.read_csv(df_scaled_path)
        else:
            print("\n⏳ Computing features... (first time only)")

            # 1. Text Embedding
            overviews = self.df_original[self.config.text_column].fillna("")
            self.embeddings = self.model.encode(overviews, show_progress_bar=True)

            # 2. Normalize numeric columns (with date handling if needed)
            df = self.df_original.copy()
            if "release_date" in self.config.numeric_columns:
                df["release_date"] = pd.to_datetime(df["release_date"], errors='coerce')
                df["release_date"] = df["release_date"].astype('int64') // 10**9
                self.df_original["release_date"] = df["release_date"]

            scaler = MinMaxScaler()
            self.numeric_scaled = scaler.fit_transform(df[self.config.numeric_columns])

            # 3. Weight genres
            genre_data = df[self.config.genre_columns].values
            self.weighted_genres = genre_data * self.config.genre_weight

            # 4. Combine features
            self.combined_features = np.hstack([
                self.embeddings,
                self.weighted_genres,
                self.numeric_scaled
            ])

            # 5. Save
            os.makedirs(os.path.dirname(combined_path), exist_ok=True)
            np.save(combined_path, self.combined_features)
            self.df_scaled = df.copy()
            self.df_scaled[self.config.numeric_columns] = self.numeric_scaled
            self.df_scaled.to_csv(df_scaled_path, index=False)
            print("✅ Features saved.")

    def recommend(self, movie_title: str):
        df = self.df_scaled
        matches = df[df['title'].str.lower() == movie_title.lower()]
        if matches.empty:
            return f"No movie found with title: '{movie_title}'"

        idx = matches.index[0]
        input_genres = df.loc[idx, self.config.genre_columns].values
        genre_overlap = (df[self.config.genre_columns].values * input_genres).sum(axis=1)

        candidate_mask = genre_overlap >= self.config.min_genre_overlap
        candidate_indices = np.where(candidate_mask)[0]

        input_feature = self.combined_features[idx].reshape(1, -1)
        candidate_features = self.combined_features[candidate_indices]
        similarity_scores = cosine_similarity(input_feature, candidate_features).flatten()

        sorted_indices = similarity_scores.argsort()[::-1][1:self.config.similarity_top_n + 1]
        recommended_indices = candidate_indices[sorted_indices]

        recommendations = self.df_original.iloc[recommended_indices][
            ['title', 'popularity', 'vote_average', 'overview']
        ].copy()
        recommendations.reset_index(drop=True, inplace=True)
        recommendations.index += 1

        recommendations['overview'] = recommendations['overview'].apply(
            lambda x: x[:150] + '...' if isinstance(x, str) and len(x) > 150 else x
        )

        return recommendations