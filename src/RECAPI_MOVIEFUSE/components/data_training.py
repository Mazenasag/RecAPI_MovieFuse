import os
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from RECAPI_MOVIEFUSE.entity.config_entity import ModelTrainingConfig


class MovieRecommender:
    def __init__(self, config:ModelTrainingConfig):
        self.config = config
        self.combined_features = None
        self.df_scaled = None
        self.df_original = None
        self.model = None

    def preprocess_and_cache(self, movie_title: str = None):
        combined_path = self.config.combined_path

        # Load original dataframe (already processed)
        self.df_original = pd.read_csv(self.config.df_original)

        if os.path.exists(combined_path):
            print("\n✅ Loading precomputed features...")
            self.combined_features = np.load(combined_path)
            # Since combined_features already includes scaled numeric + weighted genres + embeddings,
            # no need to scale numeric again, just reconstruct df_scaled from saved CSV or cache
            if self.df_scaled is None:
                self.df_scaled = self.df_original.copy()
                # If you saved scaled numeric features somewhere, load them here and assign to df_scaled
                # Otherwise, skip scaling if you don't need df_scaled for recommend
        else:
            print("\n⏳ Computing features... (first time only)")
            # Load model only here
            self.model = SentenceTransformer(self.config.model_name)

            # Embed text
            overviews = self.df_original[self.config.text_column].fillna("")
            self.embeddings = self.model.encode(overviews, show_progress_bar=True)

            # Handle date if needed and scale numeric columns
            df = self.df_original.copy()
            if "release_date" in self.config.numeric_columns:
                df["release_date"] = pd.to_datetime(df["release_date"], errors='coerce')
                df["release_date"] = df["release_date"].astype('int64') // 10**9
                self.df_original["release_date"] = df["release_date"]

            scaler = MinMaxScaler()
            self.numeric_scaled = scaler.fit_transform(df[self.config.numeric_columns])

            self.df_scaled = df.copy()
            self.df_scaled[self.config.numeric_columns] = self.numeric_scaled

            # Weight genres
            genre_data = df[self.config.genre_columns].values
            self.weighted_genres = genre_data * self.config.genre_weight

            # Combine features
            self.combined_features = np.hstack([
                self.embeddings,
                self.weighted_genres,
                self.numeric_scaled
            ])

            # Save combined features to disk
            os.makedirs(os.path.dirname(combined_path), exist_ok=True)
            np.save(combined_path, self.combined_features)
            print("✅ Features saved.")

        if movie_title:
            return self.recommend(movie_title)

    def _scale_numeric_features(self):
        # Helper to scale numeric features internally when loading features only
        df = self.df_original.copy()
        if "release_date" in self.config.numeric_columns:
            df["release_date"] = pd.to_datetime(df["release_date"], errors='coerce')
            df["release_date"] = df["release_date"].astype('int64') // 10**9

        scaler = MinMaxScaler()
        numeric_scaled = scaler.fit_transform(df[self.config.numeric_columns])

        self.df_scaled = df.copy()
        self.df_scaled[self.config.numeric_columns] = numeric_scaled


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
            ['id','title', 'popularity', 'vote_average', 'overview']
        ].copy()
        recommendations.reset_index(drop=True, inplace=True)
        recommendations.index += 1


        recommendations['overview'] = recommendations['overview'].apply(
            lambda x: x[:150] + '...' if isinstance(x, str) and len(x) > 150 else x
        )


        return recommendations
