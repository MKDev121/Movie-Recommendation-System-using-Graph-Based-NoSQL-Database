"""Graph Traversal Recommendation Engine mirroring Review 1 Section 5.5 & Section 2.1 FR-7.

Simulates pure graph traversal Cypher semantics in Python (and connects to Neo4j if configured).
Provides multi-hop path explanations:
(TargetUser) -> [:RATED] -> (PivotMovie) <- [:RATED] -> (PeerUser) -> [:RATED] -> (RecommendedMovie)
"""

from typing import Dict, List, Any
from ai_model.data import MovieDataset

class GraphTraversalRecommender:
    """Graph pattern traversal recommender as specified in Review 1 Report."""

    def __init__(self, dataset: MovieDataset):
        self.dataset = dataset

    def collaborative_graph_recommend(self, user_id: str, min_score: float = 4.0, top_n: int = 5) -> List[Dict[str, Any]]:
        """Executes Cypher equivalent of Review 1 Section 5.5:

        MATCH (target:User {userId:$userId})-[:RATED]->(m:Movie)<-[:RATED]-(other:User)
        MATCH (other)-[r:RATED]->(rec:Movie)
        WHERE NOT (target)-[:RATED]->(rec) AND r.score >= $min_score
        RETURN rec, count(*) AS strength, collect(distinct other.name) AS peers
        """
        user_ratings = self.dataset.get_user_ratings(user_id)
        # Find movies target user liked
        target_liked_movies = {m_id: score for m_id, score in user_ratings.items() if score >= min_score}

        # Step 1: Find peer users who rated the same movies >= min_score
        peer_to_pivots = {}  # peer_id -> list of shared liked movies
        for _, row in self.dataset.ratings_df.iterrows():
            other_user = row["userId"]
            m_id = row["movieId"]
            score = float(row["score"])

            if other_user != user_id and m_id in target_liked_movies and score >= min_score:
                if other_user not in peer_to_pivots:
                    peer_to_pivots[other_user] = []
                peer_to_pivots[other_user].append(m_id)

        # Step 2: Find movies those peers rated >= min_score that target hasn't rated
        candidate_scores = {}  # rec_movie_id -> list of (peer_id, score, pivot_movie_id)
        for peer_id, pivots in peer_to_pivots.items():
            peer_ratings = self.dataset.get_user_ratings(peer_id)
            for rec_movie_id, score in peer_ratings.items():
                if rec_movie_id not in user_ratings and score >= min_score:
                    if rec_movie_id not in candidate_scores:
                        candidate_scores[rec_movie_id] = []
                    candidate_scores[rec_movie_id].append({
                        "peerId": peer_id,
                        "peerName": self.dataset.user_meta[peer_id]["name"],
                        "score": score,
                        "pivotMovieId": pivots[0],
                        "pivotMovieTitle": self.dataset.movie_meta[pivots[0]]["title"]
                    })

        results = []
        for rec_id, supports in candidate_scores.items():
            meta = self.dataset.movie_meta[rec_id]
            avg_peer_score = sum(s["score"] for s in supports) / len(supports)
            strength = len(supports)

            # Build 3-hop Cypher explanation path
            first_support = supports[0]
            explanation_path = (
                f"({self.dataset.user_meta[user_id]['name']}) -[:RATED]-> "
                f"({first_support['pivotMovieTitle']}) <-[:RATED]- "
                f"({first_support['peerName']}) -[:RATED]-> ({meta['title']})"
            )

            peer_names = list({s["peerName"] for s in supports})
            results.append({
                "movieId": rec_id,
                "title": meta["title"],
                "releaseYear": meta["releaseYear"],
                "genres": meta["genres"],
                "director": meta["director"],
                "strength": strength,
                "predictedRating": round(avg_peer_score, 2),
                "model": "Graph Traversal (Review 1)",
                "graphPath": explanation_path,
                "peers": peer_names,
                "explanation": f"Recommended via {strength} graph peer path(s): {', '.join(peer_names)}"
            })

        results.sort(key=lambda x: (x["strength"], x["predictedRating"]), reverse=True)
        return results[:top_n]

    def social_graph_recommend(self, user_id: str, min_score: float = 4.0) -> List[Dict[str, Any]]:
        """Executes Social Graph recommendation (Review 1 FR-7):

        MATCH (u:User {userId:$userId})-[:FOLLOWS]->(friend:User)-[r:RATED]->(rec:Movie)
        WHERE NOT (u)-[:RATED]->(rec) AND r.score >= $min_score
        """
        follows = self.dataset.get_user_follows(user_id)
        user_ratings = self.dataset.get_user_ratings(user_id)

        recommendations = []
        for friend_id in follows:
            friend_name = self.dataset.user_meta[friend_id]["name"]
            friend_ratings = self.dataset.get_user_ratings(friend_id)

            for rec_movie_id, score in friend_ratings.items():
                if rec_movie_id not in user_ratings and score >= min_score:
                    meta = self.dataset.movie_meta[rec_movie_id]
                    recommendations.append({
                        "movieId": rec_movie_id,
                        "title": meta["title"],
                        "friendId": friend_id,
                        "friendName": friend_name,
                        "score": score,
                        "graphPath": f"({self.dataset.user_meta[user_id]['name']}) -[:FOLLOWS]-> ({friend_name}) -[:RATED]-> ({meta['title']})",
                        "explanation": f"High rating ({score} stars) by followed user {friend_name}"
                    })

        return recommendations
