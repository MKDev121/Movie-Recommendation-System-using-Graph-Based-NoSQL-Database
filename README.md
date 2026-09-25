# Framewise: Graph-Powered Movie Recommendation System

A BCSE302P Database Systems Lab project based on the submitted Review 1 design. Framewise uses Neo4j as the intended persistence layer for relationship-first recommendations between users, movies, genres, actors, directors, ratings, and follows.

## Run the demonstration

The UI is intentionally build-tool-free so it can be demonstrated on a lab machine without npm. From this folder run:

```bash
python3 -m http.server 8000
```

Open <http://localhost:8000>. The frontend includes a seeded demo mode with search, movie detail, rating and library CRUD flows, recommendation modes, and an interactive canvas graph explorer.

## Neo4j implementation

1. Start Neo4j Desktop or Neo4j Aura.
2. Run `database/schema.cypher` in Neo4j Browser.
3. Run `database/seed.cypher` to load 126 nodes and 250+ relationships.
4. Run the examples in `database/queries.cypher` for the 10 required queries and analytics.
5. Configure `NEO4J_URI`, `NEO4J_USERNAME`, and `NEO4J_PASSWORD` in the future API service. The UI demo remains available without credentials.

## Rubric mapping

- 6 labels: `User`, `Movie`, `Genre`, `Actor`, `Director`, `Review`
- 7 relationship types: `RATED`, `BELONGS_TO`, `ACTED_IN`, `DIRECTED_BY`, `FOLLOWS`, `WATCHLISTED`, `SIMILAR_TO`
- 100+ nodes: 10 users, 20 movies, 12 genres, 40 actors, 20 directors, 24 reviews in the seed script
- 10 meaningful Cypher queries in `database/queries.cypher`
- Analytics: collaborative similarity, content similarity, shortest path, and PageRank-compatible projection
- Constraints and indexes in `database/schema.cypher`
- CRUD: user, movie, rating, and watchlist queries

## Submission files

- `database/schema.cypher`: graph schema, constraints, indexes
- `database/seed.cypher`: reproducible sample data
- `database/queries.cypher`: CRUD, recommendations, search, analytics
- `REPORT.md`: final technical report and viva talking points
- `USER_MANUAL.md`: demonstration instructions
