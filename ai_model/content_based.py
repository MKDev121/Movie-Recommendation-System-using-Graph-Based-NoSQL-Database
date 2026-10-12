"""Content-Based Recommendation Model based on Review 1 FR-5.

Computes TF-IDF and metadata feature representations (genres, directors, actors, plot summary)
to construct personalized user taste vectors and compute cosine similarity against movies.
"""

from typing import Dict, List, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ai_model.data import MovieDataset

class ContentBasedRecommender:
    """Content-based recommender utilizing TF-IDF and metadata cosine similarity."""

    def __init__(self, dataset: MovieDataset):
        self.dataset = dataset
        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=300)
        self.movie_feature_matrix = None
        self.movie_ids = []
        self._fit()

    def _create_movie_soup(self, movie: Dict[str, Any]) -> str:
        """Creates a rich textual bag-of-words soup representing the movie."""
        genres_str = " ".join([g.replace(" ", "_") for g in movie.get("genres", [])] * 3)
        director_str = movie.get("director", "").replace(" ", "_") + " " + movie.get("director", "")
        director_repeated = f"{director_str} {director_str}"
        actors_str = " ".join([a.replace(" ", "_") for a in movie.get("actors", [])])
        plot_str = movie.get("plotSummary", "")

        return f"{genres_str} {director_repeated} {actors_str} {plot_str}"

    def _fit(self):
        """Builds TF-IDF feature space across all movies in catalog."""
        self.movie_ids = list(self.dataset.movie_meta.keys())
        soups = [self._create_movie_soup(self.dataset.movie_meta[m_id]) for m_id in self.movie_ids]
        self.movie_feature_matrix = self.vectorizer.fit_transform(soups).toarray()

    def get_movie_vector(self, movie_id: str) -> np.ndarray:
        if movie_id not in self.dataset.movie_meta:
            return np.zeros(self.movie_feature_matrix.shape[1])
        idx = self.movie_ids.index(movie_id)
        return self.movie_feature_matrix[idx]

    def build_user_profile(self, user_id: str) -> np.ndarray:
        """Constructs a user taste profile as a rating-weighted average of movie vectors."""
        user_ratings = self.dataset.get_user_ratings(user_id)
        if not user_ratings:
            # Fallback to mean vector if user has no ratings
            return np.mean(self.movie_feature_matrix, axis=0)

        profile = np.zeros(self.movie_feature_matrix.shape[1], dtype=np.float32)
        total_weight = 0.0

        for m_id, score in user_ratings.items():
            if m_id in self.movie_ids:
                weight = max(0.1, score - 2.5)  # ratings >= 3 count positively
                idx = self.movie_ids.index(m_id)
                profile += weight * self.movie_feature_matrix[idx]
                total_weight += weight

        if total_weight > 0:
            profile /= total_weight

        norm = np.linalg.norm(profile)
        if norm > 0:
            profile /= norm
        return profile

    def find_matched_features(self, user_id: str, candidate_movie_id: str) -> List[str]:
        """Identifies specific genres, directors, and actors shared with user's top-rated movies."""
        user_ratings = self.dataset.get_user_ratings(user_id)
        cand_meta = self.dataset.movie_meta.get(candidate_movie_id, {})
        cand_genres = set(cand_meta.get("genres", []))
        cand_director = cand_meta.get("director")
        cand_actors = set(cand_meta.get("actors", []))

        matches = []
        for liked_id, score in user_ratings.items():
            if score >= 4.0 and liked_id in self.dataset.movie_meta:
                liked_meta = self.dataset.movie_meta[liked_id]
                shared_genres = cand_genres.intersection(set(liked_meta.get("genres", [])))
                shared_director = (cand_director == liked_meta.get("director")) and cand_director
                shared_actors = cand_actors.intersection(set(liked_meta.get("actors", [])))

                if shared_director:
                    matches.append(f"Directed by {cand_director} (like '{liked_meta['title']}')")
                if shared_genres:
                    matches.append(f"Shares {', '.join(shared_genres)} genre with '{liked_meta['title']}'")
                if shared_actors:
                    matches.append(f"Stars {', '.join(shared_actors)} (like '{liked_meta['title']}')")

        # Deduplicate while preserving order
        unique_matches = []
        for m in matches:
            if m not in unique_matches:
                unique_matches.append(m)
        return unique_matches

    def recommend(self, user_id: str, top_n: int = 5) -> List[Dict[str, Any]]:
        """Returns Top-N content-based recommendations ranked by cosine similarity."""
        user_profile = self.build_user_profile(user_id).reshape(1, -1)
        sims = cosine_similarity(user_profile, self.movie_feature_matrix)[0]

        user_rated = self.dataset.get_user_ratings(user_id)
        scored = []

        for idx, m_id in enumerate(self.movie_ids):
            if m_id in user_rated:
                continue

            similarity_score = float(sims[idx])
            meta = self.dataset.movie_meta[m_id]
            matched = self.find_matched_features(user_id, m_id)

            explanation = matched[0] if matched else f"Matches your preferred themes in {', '.join(meta.get('genres', []))}"

            # Convert cosine sim [0, 1] to predicted rating scale [1.0, 5.0]
            predicted_rating = round(3.0 + similarity_score * 2.0, 2)

            scored.append({
                "movieId": m_id,
                "title": meta["title"],
                "releaseYear": meta["releaseYear"],
                "genres": meta["genres"],
                "director": meta["director"],
                "actors": meta["actors"],
                "similarityScore": round(similarity_score, 4),
                "predictedRating": min(5.0, predicted_rating),
                "model": "Content-Based (TF-IDF)",
                "explanation": explanation,
                "matchedFeatures": matched
            })

        scored.sort(key=lambda x: x["similarityScore"], reverse=True)
        return scored[:top_n]
