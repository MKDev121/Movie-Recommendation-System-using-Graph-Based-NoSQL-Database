"""Data definitions and dataset loader based on Review 1 Report and Seed specifications.

Entities:
- Users (userId, name, age, email)
- Movies (movieId, title, year, genres, director, actors, plot)
- Ratings (userId, movieId, score [1-5], timestamp)
- Social Follows (userId, followedUserId)
"""

from typing import Dict, List, Any
import pandas as pd
import numpy as np

# Review 1 Table 5.1, 5.2, 5.3 exact dataset
REVIEW1_USERS = [
    {"userId": "U1", "name": "Aditi Sharma", "age": 24, "email": "aditi@example.com", "joinDate": "2024-01-15"},
    {"userId": "U2", "name": "Rahul Verma", "age": 29, "email": "rahul@example.com", "joinDate": "2024-02-03"},
    {"userId": "U3", "name": "Sneha Iyer", "age": 21, "email": "sneha@example.com", "joinDate": "2024-03-10"},
    {"userId": "U4", "name": "Karthik Raja", "age": 27, "email": "karthik@example.com", "joinDate": "2024-04-22"},
]

REVIEW1_MOVIES = [
    {
        "movieId": "M1",
        "title": "Inception",
        "releaseYear": 2010,
        "genres": ["Sci-Fi", "Thriller"],
        "director": "Christopher Nolan",
        "actors": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"],
        "plotSummary": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
    },
    {
        "movieId": "M2",
        "title": "The Shawshank Redemption",
        "releaseYear": 1994,
        "genres": ["Drama"],
        "director": "Frank Darabont",
        "actors": ["Tim Robbins", "Morgan Freeman", "Bob Gunton"],
        "plotSummary": "Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion."
    },
    {
        "movieId": "M3",
        "title": "Interstellar",
        "releaseYear": 2014,
        "genres": ["Sci-Fi", "Drama"],
        "director": "Christopher Nolan",
        "actors": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
        "plotSummary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot is tasked to pilot a spacecraft to find a new home for mankind."
    },
    {
        "movieId": "M4",
        "title": "The Dark Knight",
        "releaseYear": 2008,
        "genres": ["Action", "Crime", "Drama"],
        "director": "Christopher Nolan",
        "actors": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
        "plotSummary": "When the menace known as the Joker wreaks havoc and chaos on Gotham, Batman must accept one of the greatest psychological and physical tests."
    },
    {
        "movieId": "M5",
        "title": "3 Idiots",
        "releaseYear": 2009,
        "genres": ["Comedy", "Drama"],
        "director": "Rajkumar Hirani",
        "actors": ["Aamir Khan", "Madhavan", "Sharman Joshi", "Kareena Kapoor"],
        "plotSummary": "Two friends search for their long lost companion while revisiting their college days and memories of their friend who inspired them to think differently."
    }
]

REVIEW1_RATINGS = [
    {"userId": "U1", "movieId": "M1", "score": 5.0, "timestamp": "2024-05-01"},
    {"userId": "U1", "movieId": "M3", "score": 4.0, "timestamp": "2024-05-04"},
    {"userId": "U2", "movieId": "M1", "score": 4.0, "timestamp": "2024-05-02"},
    {"userId": "U2", "movieId": "M4", "score": 5.0, "timestamp": "2024-05-05"},
    {"userId": "U3", "movieId": "M2", "score": 5.0, "timestamp": "2024-05-03"},
    {"userId": "U4", "movieId": "M3", "score": 5.0, "timestamp": "2024-05-06"},
]

REVIEW1_FOLLOWS = [
    {"userId": "U1", "follows": "U2", "since": "2024-02-10"},
    {"userId": "U4", "follows": "U1", "since": "2024-04-25"},
]

# Expanded Catalog adhering to Review 1 Graph Design and Project Seed
EXPANDED_MOVIES = [
    {
        "movieId": "m1",
        "title": "Past Lives",
        "releaseYear": 2023,
        "genres": ["Romance", "Drama"],
        "director": "Celine Song",
        "actors": ["Greta Lee", "Teo Yoo", "John Magaro"],
        "plotSummary": "Nora and Hae Sung, two deeply connected childhood friends, are wrested apart after Nora's family emigrates from South Korea. Two decades later, they are reunited in New York for one fateful week."
    },
    {
        "movieId": "m2",
        "title": "The Holdovers",
        "releaseYear": 2023,
        "genres": ["Comedy", "Drama"],
        "director": "Alexander Payne",
        "actors": ["Paul Giamatti", "Da'Vine Joy Randolph", "Dominic Sessa"],
        "plotSummary": "A curmudgeonly instructor at a New England prep school remains on campus during Christmas break to babysit the handful of students with nowhere to go."
    },
    {
        "movieId": "m3",
        "title": "Aftersun",
        "releaseYear": 2022,
        "genres": ["Drama"],
        "director": "Charlotte Wells",
        "actors": ["Paul Mescal", "Frankie Corio", "Celia Rowlson-Hall"],
        "plotSummary": "Sophie reflects on the shared joy and private melancholy of a holiday she took with her father twenty years earlier as she tries to reconcile the father she knew with the man she didn't."
    },
    {
        "movieId": "m4",
        "title": "The Worst Person in the World",
        "releaseYear": 2021,
        "genres": ["Romance", "Comedy", "Drama"],
        "director": "Joachim Trier",
        "actors": ["Renate Reinsve", "Anders Danielsen Lie", "Herbert Nordrum"],
        "plotSummary": "A young woman navigates the troubled waters of her love life and struggles to find her career path, leading her to take a realistic look at who she really is."
    },
    {
        "movieId": "m5",
        "title": "Anatomy of a Fall",
        "releaseYear": 2023,
        "genres": ["Drama", "Mystery", "Crime"],
        "director": "Justine Triet",
        "actors": ["Sandra Hüller", "Swann Arlaud", "Milo Machado Graner"],
        "plotSummary": "A woman is suspected of murder after her husband's death in the snow in a secluded chalet, and their half-blind son faces a moral dilemma as the main witness."
    },
    {
        "movieId": "m6",
        "title": "The Grand Budapest Hotel",
        "releaseYear": 2014,
        "genres": ["Comedy", "Adventure"],
        "director": "Wes Anderson",
        "actors": ["Ralph Fiennes", "Tony Revolori", "Adrien Brody", "Willem Dafoe"],
        "plotSummary": "A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy in the hotel's glorious golden years."
    },
    {
        "movieId": "m7",
        "title": "Decision to Leave",
        "releaseYear": 2022,
        "genres": ["Mystery", "Romance", "Drama"],
        "director": "Park Chan-wook",
        "actors": ["Park Hae-il", "Tang Wei", "Lee Jung-hyun"],
        "plotSummary": "A detective investigating a man's death in the mountains meets the dead man's mysterious wife in the course of his investigation and begins to develop an obsession with her."
    },
    {
        "movieId": "m8",
        "title": "Perfect Days",
        "releaseYear": 2023,
        "genres": ["Drama"],
        "director": "Wim Wenders",
        "actors": ["Koji Yakusho", "Tokio Emoto", "Arisa Nakano"],
        "plotSummary": "Hirayama seems entirely content with his simple life as a cleaner of toilets in Tokyo. Outside of his very structured everyday routine, he enjoys his passion for music and books."
    },
    {
        "movieId": "m9",
        "title": "Spider-Man: Across the Spider-Verse",
        "releaseYear": 2023,
        "genres": ["Animation", "Action", "Adventure", "Sci-Fi"],
        "director": "Joaquim Dos Santos",
        "actors": ["Shameik Moore", "Hailee Steinfeld", "Oscar Isaac", "Daniel Kaluuya"],
        "plotSummary": "Miles Morales catapults across the Multiverse, where he encounters a team of Spider-People charged with protecting its very existence."
    },
    {
        "movieId": "m10",
        "title": "Oppenheimer",
        "releaseYear": 2023,
        "genres": ["Drama", "History", "Biography"],
        "director": "Christopher Nolan",
        "actors": ["Cillian Murphy", "Emily Blunt", "Matt Damon", "Robert Downey Jr."],
        "plotSummary": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during the Manhattan Project."
    },
    {
        "movieId": "m11",
        "title": "The Farewell",
        "releaseYear": 2019,
        "genres": ["Comedy", "Drama"],
        "director": "Lulu Wang",
        "actors": ["Awkwafina", "Tzi Ma", "Diana Lin", "Zhao Shu-zhen"],
        "plotSummary": "A Chinese-American family discovers their grandmother has only a short time left to live and decide to keep her in the dark while scheduling an impromptu wedding."
    },
    {
        "movieId": "m12",
        "title": "Arrival",
        "releaseYear": 2016,
        "genres": ["Sci-Fi", "Drama", "Mystery"],
        "director": "Denis Villeneuve",
        "actors": ["Amy Adams", "Jeremy Renner", "Forest Whitaker"],
        "plotSummary": "A linguist works with the military to communicate with alien lifeforms after twelve mysterious spacecraft appear around the world."
    },
    {
        "movieId": "m13",
        "title": "Moonlight",
        "releaseYear": 2016,
        "genres": ["Drama"],
        "director": "Barry Jenkins",
        "actors": ["Mahershala Ali", "Naomie Harris", "Trevante Rhodes", "Ashton Sanders"],
        "plotSummary": "A young African-American man grapples with his identity and sexuality while experiencing the everyday struggles of childhood, adolescence, and burgeoning adulthood."
    },
    {
        "movieId": "m14",
        "title": "Whiplash",
        "releaseYear": 2014,
        "genres": ["Drama", "Music"],
        "director": "Damien Chazelle",
        "actors": ["Miles Teller", "J.K. Simmons", "Paul Reiser"],
        "plotSummary": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student's potential."
    },
    {
        "movieId": "m15",
        "title": "Portrait of a Lady on Fire",
        "releaseYear": 2019,
        "genres": ["Drama", "Romance", "History"],
        "director": "Céline Sciamma",
        "actors": ["Noémie Merlant", "Adèle Haenel", "Luàna Bajrami"],
        "plotSummary": "On an isolated island in Brittany at the end of the eighteenth century, a female painter is obliged to paint a wedding portrait of a young woman secretly."
    },
    {
        "movieId": "m16",
        "title": "Her",
        "releaseYear": 2013,
        "genres": ["Drama", "Romance", "Sci-Fi"],
        "director": "Spike Jonze",
        "actors": ["Joaquin Phoenix", "Scarlett Johansson", "Amy Adams", "Rooney Mara"],
        "plotSummary": "In a near future, a lonely writer develops an unlikely relationship with an operating system designed to meet his every need."
    },
    {
        "movieId": "m17",
        "title": "Parasite",
        "releaseYear": 2019,
        "genres": ["Drama", "Thriller", "Comedy"],
        "director": "Bong Joon Ho",
        "actors": ["Song Kang-ho", "Lee Sun-kyun", "Cho Yeo-jeong", "Choi Woo-shik"],
        "plotSummary": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan."
    },
    {
        "movieId": "m18",
        "title": "The Handmaiden",
        "releaseYear": 2016,
        "genres": ["Drama", "Romance", "Thriller"],
        "director": "Park Chan-wook",
        "actors": ["Kim Min-hee", "Kim Tae-ri", "Ha Jung-woo", "Cho Jin-woong"],
        "plotSummary": "A woman is hired as a handmaiden to an eccentric Japanese heiress, but secretly she is involved in a plot to defraud her."
    },
    {
        "movieId": "m19",
        "title": "Before Sunrise",
        "releaseYear": 1995,
        "genres": ["Drama", "Romance"],
        "director": "Richard Linklater",
        "actors": ["Ethan Hawke", "Julie Delpy", "Andrea Eckert"],
        "plotSummary": "A young man and woman meet on a train in Europe, and wind up spending one evening together in Vienna. Unfortunately, both know this will probably be their only night together."
    },
    {
        "movieId": "m20",
        "title": "The Secret Life of Walter Mitty",
        "releaseYear": 2013,
        "genres": ["Adventure", "Comedy", "Drama"],
        "director": "Ben Stiller",
        "actors": ["Ben Stiller", "Kristen Wiig", "Jon Daly", "Sean Penn"],
        "plotSummary": "When both he and a colleague are about to lose their jobs, Walter takes action by embarking on an adventure more extraordinary than anything he could have ever imagined."
    }
]

EXPANDED_USERS = [
    {"userId": "u1", "name": "Meet Kareliya", "age": 21, "email": "viewer1@framewise.demo", "joinDate": "2026-08-11"},
    {"userId": "u2", "name": "Harshit Pandey", "age": 22, "email": "viewer2@framewise.demo", "joinDate": "2026-08-12"},
    {"userId": "u3", "name": "Manik Chauhan", "age": 22, "email": "viewer3@framewise.demo", "joinDate": "2026-08-13"},
    {"userId": "u4", "name": "Aditi Sharma", "age": 24, "email": "viewer4@framewise.demo", "joinDate": "2026-08-14"},
    {"userId": "u5", "name": "Rahul Verma", "age": 29, "email": "viewer5@framewise.demo", "joinDate": "2026-08-15"},
    {"userId": "u6", "name": "Sneha Iyer", "age": 21, "email": "viewer6@framewise.demo", "joinDate": "2026-08-16"},
    {"userId": "u7", "name": "Karthik Raja", "age": 27, "email": "viewer7@framewise.demo", "joinDate": "2026-08-17"},
    {"userId": "u8", "name": "Priya Nair", "age": 25, "email": "viewer8@framewise.demo", "joinDate": "2026-08-18"},
    {"userId": "u9", "name": "Rohan Mehta", "age": 26, "email": "viewer9@framewise.demo", "joinDate": "2026-08-19"},
    {"userId": "u10", "name": "Ananya Sen", "age": 23, "email": "viewer10@framewise.demo", "joinDate": "2026-08-20"},
]

# Dense user-item rating network simulating realistic preference clusters
EXPANDED_RATINGS = [
    # u1 (Meet) - Loves intimate dramas, romance, and artistic cinematography
    {"userId": "u1", "movieId": "m1", "score": 5.0, "timestamp": "2026-09-01"},
    {"userId": "u1", "movieId": "m3", "score": 5.0, "timestamp": "2026-09-02"},
    {"userId": "u1", "movieId": "m6", "score": 4.0, "timestamp": "2026-09-03"},
    {"userId": "u1", "movieId": "m8", "score": 4.5, "timestamp": "2026-09-04"},
    {"userId": "u1", "movieId": "m15", "score": 5.0, "timestamp": "2026-09-05"},
    {"userId": "u1", "movieId": "m19", "score": 4.5, "timestamp": "2026-09-06"},
    # u2 (Harshit) - Loves Sci-Fi, thrillers, Christopher Nolan, Denis Villeneuve
    {"userId": "u2", "movieId": "m10", "score": 5.0, "timestamp": "2026-09-02"},
    {"userId": "u2", "movieId": "m12", "score": 5.0, "timestamp": "2026-09-03"},
    {"userId": "u2", "movieId": "m16", "score": 4.5, "timestamp": "2026-09-04"},
    {"userId": "u2", "movieId": "m17", "score": 5.0, "timestamp": "2026-09-05"},
    {"userId": "u2", "movieId": "m9", "score": 4.0, "timestamp": "2026-09-06"},
    {"userId": "u2", "movieId": "m5", "score": 4.5, "timestamp": "2026-09-07"},
    # u3 (Manik) - Loves high-intensity drama, music, mystery
    {"userId": "u3", "movieId": "m14", "score": 5.0, "timestamp": "2026-09-02"},
    {"userId": "u3", "movieId": "m5", "score": 4.5, "timestamp": "2026-09-03"},
    {"userId": "u3", "movieId": "m7", "score": 4.5, "timestamp": "2026-09-04"},
    {"userId": "u3", "movieId": "m18", "score": 5.0, "timestamp": "2026-09-05"},
    {"userId": "u3", "movieId": "m17", "score": 4.5, "timestamp": "2026-09-06"},
    {"userId": "u3", "movieId": "m10", "score": 4.0, "timestamp": "2026-09-07"},
    # u4 (Aditi) - Overlaps with Meet (Romance, Drama)
    {"userId": "u4", "movieId": "m1", "score": 5.0, "timestamp": "2026-09-03"},
    {"userId": "u4", "movieId": "m4", "score": 4.5, "timestamp": "2026-09-04"},
    {"userId": "u4", "movieId": "m15", "score": 4.5, "timestamp": "2026-09-05"},
    {"userId": "u4", "movieId": "m19", "score": 5.0, "timestamp": "2026-09-06"},
    {"userId": "u4", "movieId": "m2", "score": 4.0, "timestamp": "2026-09-07"},
    # u5 (Rahul) - Overlaps with Harshit (Sci-Fi, Nolan)
    {"userId": "u5", "movieId": "m10", "score": 4.5, "timestamp": "2026-09-04"},
    {"userId": "u5", "movieId": "m12", "score": 4.5, "timestamp": "2026-09-05"},
    {"userId": "u5", "movieId": "m9", "score": 5.0, "timestamp": "2026-09-06"},
    {"userId": "u5", "movieId": "m14", "score": 4.0, "timestamp": "2026-09-07"},
    {"userId": "u5", "movieId": "m20", "score": 4.5, "timestamp": "2026-09-08"},
    # u6 (Sneha) - Eclectic (Dramas, Mystery, Comedy)
    {"userId": "u6", "movieId": "m2", "score": 5.0, "timestamp": "2026-09-05"},
    {"userId": "u6", "movieId": "m6", "score": 4.5, "timestamp": "2026-09-06"},
    {"userId": "u6", "movieId": "m7", "score": 4.0, "timestamp": "2026-09-07"},
    {"userId": "u6", "movieId": "m11", "score": 5.0, "timestamp": "2026-09-08"},
    {"userId": "u6", "movieId": "m3", "score": 4.0, "timestamp": "2026-09-09"},
    # u7 (Karthik) - Thriller, Korean Cinema, Mystery
    {"userId": "u7", "movieId": "m7", "score": 5.0, "timestamp": "2026-09-06"},
    {"userId": "u7", "movieId": "m17", "score": 5.0, "timestamp": "2026-09-07"},
    {"userId": "u7", "movieId": "m18", "score": 4.5, "timestamp": "2026-09-08"},
    {"userId": "u7", "movieId": "m5", "score": 4.0, "timestamp": "2026-09-09"},
    {"userId": "u7", "movieId": "m14", "score": 4.5, "timestamp": "2026-09-10"},
    # u8 (Priya) - Intimate storytelling & character studies
    {"userId": "u8", "movieId": "m3", "score": 5.0, "timestamp": "2026-09-07"},
    {"userId": "u8", "movieId": "m8", "score": 5.0, "timestamp": "2026-09-08"},
    {"userId": "u8", "movieId": "m13", "score": 4.5, "timestamp": "2026-09-09"},
    {"userId": "u8", "movieId": "m1", "score": 4.5, "timestamp": "2026-09-10"},
    {"userId": "u8", "movieId": "m11", "score": 4.0, "timestamp": "2026-09-11"},
    # u9 (Rohan) - Wes Anderson, Feel-good, Comedy
    {"userId": "u9", "movieId": "m6", "score": 5.0, "timestamp": "2026-09-08"},
    {"userId": "u9", "movieId": "m2", "score": 4.5, "timestamp": "2026-09-09"},
    {"userId": "u9", "movieId": "m20", "score": 4.5, "timestamp": "2026-09-10"},
    {"userId": "u9", "movieId": "m11", "score": 4.0, "timestamp": "2026-09-11"},
    # u10 (Ananya) - Sci-Fi, Romance, Philosophical
    {"userId": "u10", "movieId": "m16", "score": 5.0, "timestamp": "2026-09-09"},
    {"userId": "u10", "movieId": "m12", "score": 4.5, "timestamp": "2026-09-10"},
    {"userId": "u10", "movieId": "m1", "score": 4.5, "timestamp": "2026-09-11"},
    {"userId": "u10", "movieId": "m19", "score": 4.0, "timestamp": "2026-09-12"},
]

EXPANDED_FOLLOWS = [
    {"userId": "u1", "follows": "u4", "since": "2026-08-20"},
    {"userId": "u1", "follows": "u8", "since": "2026-08-22"},
    {"userId": "u2", "follows": "u5", "since": "2026-08-21"},
    {"userId": "u3", "follows": "u7", "since": "2026-08-25"},
    {"userId": "u4", "follows": "u1", "since": "2026-08-26"},
    {"userId": "u5", "follows": "u2", "since": "2026-08-27"},
]

class MovieDataset:
    """Manages tabular representations and matrices for recommendation models."""
    def __init__(self, mode: str = "expanded"):
        if mode == "review1":
            self.users_data = REVIEW1_USERS
            self.movies_data = REVIEW1_MOVIES
            self.ratings_data = REVIEW1_RATINGS
            self.follows_data = REVIEW1_FOLLOWS
        else:
            self.users_data = EXPANDED_USERS
            self.movies_data = EXPANDED_MOVIES
            self.ratings_data = EXPANDED_RATINGS
            self.follows_data = EXPANDED_FOLLOWS

        self.users_df = pd.DataFrame(self.users_data)
        self.movies_df = pd.DataFrame(self.movies_data)
        self.ratings_df = pd.DataFrame(self.ratings_data)
        self.follows_df = pd.DataFrame(self.follows_data)

        # Index mappings
        self.user_to_idx = {u: i for i, u in enumerate(self.users_df["userId"].unique())}
        self.idx_to_user = {i: u for u, i in self.user_to_idx.items()}

        self.movie_to_idx = {m: i for i, m in enumerate(self.movies_df["movieId"].unique())}
        self.idx_to_movie = {i: m for m, i in self.movie_to_idx.items()}

        self.movie_meta = {m["movieId"]: m for m in self.movies_data}
        self.user_meta = {u["userId"]: u for u in self.users_data}

    def build_user_item_matrix(self) -> np.ndarray:
        """Constructs an R matrix of shape (n_users, n_movies) with rating values."""
        n_users = len(self.user_to_idx)
        n_movies = len(self.movie_to_idx)
        R = np.zeros((n_users, n_movies), dtype=np.float32)

        for _, row in self.ratings_df.iterrows():
            u_idx = self.user_to_idx.get(row["userId"])
            m_idx = self.movie_to_idx.get(row["movieId"])
            if u_idx is not None and m_idx is not None:
                R[u_idx, m_idx] = float(row["score"])
        return R

    def get_user_ratings(self, user_id: str) -> Dict[str, float]:
        sub = self.ratings_df[self.ratings_df["userId"] == user_id]
        return dict(zip(sub["movieId"], sub["score"]))

    def get_user_follows(self, user_id: str) -> List[str]:
        sub = self.follows_df[self.follows_df["userId"] == user_id]
        return sub["follows"].tolist()
