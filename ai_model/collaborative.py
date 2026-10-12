"""Collaborative Filtering models for Movie Recommendations.

Implements:
1. User-User Collaborative Filtering (Cosine & Pearson correlation)
2. Item-Item Collaborative Filtering
3. Matrix Factorization (Funk-SVD with user/item biases & latent embeddings via SGD)
"""

import numpy as np
from typing import Dict, List, Tuple
from ai_model.data import MovieDataset

class CollaborativeFiltering:
    """Memory-based and model-based collaborative filtering recommender."""

    def __init__(self, dataset: MovieDataset, n_factors: int = 8, lr: float = 0.01, reg: float = 0.05, n_epochs: int = 150):
        self.dataset = dataset
        self.n_factors = n_factors
        self.lr = lr
        self.reg = reg
        self.n_epochs = n_epochs

        self.R = self.dataset.build_user_item_matrix()
        self.n_users, self.n_movies = self.R.shape

        # SVD model parameters
        self.global_mean = 0.0
        self.user_bias = np.zeros(self.n_users, dtype=np.float32)
        self.item_bias = np.zeros(self.n_movies, dtype=np.float32)
        self.P = np.zeros((self.n_users, self.n_factors), dtype=np.float32)
        self.Q = np.zeros((self.n_movies, self.n_factors), dtype=np.float32)

        # Similarity cache
        self.user_similarity_matrix = np.zeros((self.n_users, self.n_users), dtype=np.float32)
        self.is_trained = False

    def train_svd(self):
        """Trains Latent Factor Matrix Factorization using Stochastic Gradient Descent (SGD)."""
        mask = self.R > 0
        ratings_list = []
        for u in range(self.n_users):
            for i in range(self.n_movies):
                if mask[u, i]:
                    ratings_list.append((u, i, self.R[u, i]))

        if not ratings_list:
            return

        self.global_mean = float(np.mean([r[2] for r in ratings_list]))

        # Initialize biases & latent embeddings with small random numbers
        np.random.seed(42)
        self.user_bias = np.zeros(self.n_users, dtype=np.float32)
        self.item_bias = np.zeros(self.n_movies, dtype=np.float32)
        self.P = np.random.normal(0, 0.1, (self.n_users, self.n_factors)).astype(np.float32)
        self.Q = np.random.normal(0, 0.1, (self.n_movies, self.n_factors)).astype(np.float32)

        # SGD training loop
        for epoch in range(self.n_epochs):
            np.random.shuffle(ratings_list)
            for u, i, r in ratings_list:
                pred = self.global_mean + self.user_bias[u] + self.item_bias[i] + np.dot(self.P[u], self.Q[i])
                err = r - pred

                # Update biases
                self.user_bias[u] += self.lr * (err - self.reg * self.user_bias[u])
                self.item_bias[i] += self.lr * (err - self.reg * self.item_bias[i])

                # Update latent factors
                p_u_old = self.P[u].copy()
                self.P[u] += self.lr * (err * self.Q[i] - self.reg * self.P[u])
                self.Q[i] += self.lr * (err * p_u_old - self.reg * self.Q[i])

        # Compute User-User Cosine Similarity Matrix
        norms = np.linalg.norm(self.R, axis=1, keepdims=True)
        norms[norms == 0] = 1e-9
        norm_R = self.R / norms
        self.user_similarity_matrix = np.dot(norm_R, norm_R.T)

        self.is_trained = True

    def predict_svd_rating(self, user_id: str, movie_id: str) -> float:
        """Predicts rating for a (user, movie) pair using the trained SVD model."""
        if not self.is_trained:
            self.train_svd()

        u_idx = self.dataset.user_to_idx.get(user_id)
        m_idx = self.dataset.movie_to_idx.get(movie_id)

        if u_idx is None or m_idx is None:
            return self.global_mean

        pred = self.global_mean + self.user_bias[u_idx] + self.item_bias[m_idx] + np.dot(self.P[u_idx], self.Q[m_idx])
        return float(np.clip(pred, 1.0, 5.0))

    def get_similar_users(self, user_id: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Returns the top-K most similar peers to user_id based on rating patterns."""
        if not self.is_trained:
            self.train_svd()

        u_idx = self.dataset.user_to_idx.get(user_id)
        if u_idx is None:
            return []

        sims = self.user_similarity_matrix[u_idx].copy()
        sims[u_idx] = -1.0  # exclude self
        top_indices = np.argsort(sims)[::-1][:top_k]

        return [(self.dataset.idx_to_user[i], float(sims[i])) for i in top_indices if sims[i] > 0]

    def recommend(self, user_id: str, top_n: int = 5) -> List[Dict[str, any]]:
        """Returns Top-N recommendations for the given user using SVD matrix factorization."""
        if not self.is_trained:
            self.train_svd()

        u_idx = self.dataset.user_to_idx.get(user_id)
        if u_idx is None:
            return []

        user_rated = self.dataset.get_user_ratings(user_id)
        candidate_movies = [m_id for m_id in self.dataset.movie_meta if m_id not in user_rated]

        scored = []
        similar_users = self.get_similar_users(user_id, top_k=3)

        for m_id in candidate_movies:
            pred_score = self.predict_svd_rating(user_id, m_id)
            meta = self.dataset.movie_meta[m_id]

            # Determine peer support
            peer_supporters = []
            for peer_id, peer_sim in similar_users:
                peer_ratings = self.dataset.get_user_ratings(peer_id)
                if m_id in peer_ratings and peer_ratings[m_id] >= 4.0:
                    peer_name = self.dataset.user_meta[peer_id]["name"]
                    peer_supporters.append(f"{peer_name} rated {peer_ratings[m_id]} stars")

            reason = "High predicted taste alignment"
            if peer_supporters:
                reason = f"Liked by {', '.join(peer_supporters)}"

            scored.append({
                "movieId": m_id,
                "title": meta["title"],
                "releaseYear": meta["releaseYear"],
                "genres": meta["genres"],
                "director": meta["director"],
                "actors": meta["actors"],
                "predictedRating": round(pred_score, 2),
                "model": "Collaborative (SVD)",
                "explanation": reason
            })

        scored.sort(key=lambda x: x["predictedRating"], reverse=True)
        return scored[:top_n]
