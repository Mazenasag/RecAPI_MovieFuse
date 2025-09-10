import sys
import os

# Add src folder to sys.path so imports work
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from flask import Flask, request, render_template, send_from_directory
from RECAPI_MOVIEFUSE.components.data_training import MovieRecommender
from RECAPI_MOVIEFUSE.entity.config_entity import ModelTrainingConfig
import pandas as pd

# Create Flask app
application = Flask(__name__)
app = application

# Route to serve image files from artifacts/images/
@app.route('/artifacts/images/<path:filename>')
def serve_artifact_image(filename):
    return send_from_directory('artifacts/images', filename)

# Initialize config
config = ModelTrainingConfig(
    df_original="data/processed_data/processed_data.csv",
    combined_path="artifacts/combined_features.npy",
    model_name="all-MiniLM-L6-v2",
    text_column="overview",
    numeric_columns=["popularity", "vote_average", "vote_count", "release_date"],
    genre_columns=[
        "Adventure", "Fantasy", "Animation", "Drama", "Horror", "Action", "Comedy", "History",
        "Western", "Thriller", "Crime", "Documentary", "Science Fiction", "Mystery", "Music",
        "Romance", "Family", "War", "TV Movie"
    ],
    genre_weight=5,
    similarity_top_n=5,
    min_genre_overlap=1
)

# Load dataset once at startup
df = pd.read_csv(config.df_original)

# Initialize recommender
recommender = MovieRecommender(config)
recommender.preprocess_and_cache()

# Main route
@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = None
    input_title = None
    error = None
    recs_list = []

    if request.method == 'POST':
        input_title = request.form.get('title')
        matched = df[df['title'].str.lower() == input_title.lower()]

        if matched.empty:
            error = "Title not found in dataset."
        else:
            recommendations = recommender.recommend(input_title)

            if isinstance(recommendations, str):
                error = recommendations
                recommendations = None
            elif recommendations is not None and recommendations.empty:
                error = "No recommendations found."
                recommendations = None
            else:
                recommendations['image'] = recommendations['id'].astype(str).map(
                    lambda x: f'/artifacts/images/{x}.jpg'
                )
                recs_list = recommendations.to_dict(orient='records')

    return render_template(
        'index.html',
        recommendations=recs_list,
        has_recommendations=bool(recs_list),
        title=input_title,
        error=error
    )

# Entry point for local dev

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
