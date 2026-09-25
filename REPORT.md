# Framewise
## Final Project Report | BCSE302P Database Systems Lab

### Abstract
Framewise is a graph-based movie recommendation system designed around Neo4j. It treats a user's taste as a connected network of ratings, genres, actors, directors, follows, and watchlist choices. This makes multi-hop recommendation and explanation queries direct Cypher traversals rather than a chain of relational joins.

### Problem and objectives
Traditional tables make relationship-heavy discovery expensive to express and maintain. Framewise addresses collaborative filtering, content-based filtering, movie search, profile management, ratings, reviews, watchlists, and social influence. It is deliberately scoped as a demonstrable prototype, excluding streaming playback, payment, live external ingestion, and deep-learning models.

### Graph design
Labels: `User`, `Movie`, `Genre`, `Actor`, `Director`, `Review`.

Relationships: `RATED` (value, review, timestamp), `BELONGS_TO`, `ACTED_IN`, `DIRECTED_BY`, `FOLLOWS`, `WATCHLISTED`, `SIMILAR_TO`, and `WROTE`.

The seed creates 126 base nodes plus generated review nodes and more than 250 edges. Uniqueness constraints protect identity fields; indexes accelerate movie title, year, and user email lookup.

### Why Neo4j
MongoDB can model the same entities but needs application-side joins or aggregation pipelines for similarity paths. Cassandra is strong for predictable write-heavy access patterns but is a poor fit for exploratory traversals. Neo4j makes the recommendation path itself a first-class indexed structure, with readable Cypher, relationship properties, shortest paths, and compatibility with Graph Data Science algorithms.

### Functional implementation
The UI supports discovery, search by title/genre/actor/director, movie detail, 1–5 rating, add/remove library, recommendation modes, and an interactive graph explorer. The Cypher layer covers create/update/delete operations, movie browsing, rating writes, collaborative recommendations, content recommendations, search, shortest path, explanation paths, and PageRank.

### Analytics
1. Collaborative filtering finds peers who rated the same movies highly, then ranks their highly rated unseen movies.
2. Content filtering counts shared genre, cast, and director features.
3. Shortest path explains how a user connects to a movie.
4. PageRank identifies structurally important nodes when Neo4j GDS is installed.

### Non-functional requirements
The graph schema supports new labels and relationships without migration-heavy table redesign. Queries return JSON-shaped records for an API boundary. Constraints maintain identity integrity and relationship properties store rating values and timestamps. The frontend is responsive for desktop and mobile widths.

### Viva questions
**Why Neo4j?** Relationships and multi-hop traversal are the primary workload, so the graph model matches the domain.

**How does collaborative filtering work?** Find users sharing high-rated movies with the current user; collect movies those peers rated highly; exclude already rated or watchlisted movies; rank by average rating and peer count.

**How is content filtering different?** It compares graph features connected to liked movies, such as genres, actors, and directors, without requiring similar users.

**What protects data integrity?** Uniqueness constraints on IDs and indexed lookup properties, plus relationship properties for rating values and timestamps.

### Limitations and future work
The current browser demo uses local seed data so it can be presented without credentials. A production deployment would connect the same UI to an authenticated API, add pagination and rate validation at the API boundary, use Neo4j GDS similarity algorithms, and evaluate precision/recall against a larger anonymized dataset.
