# Framewise User Manual

## Start
Run `python3 -m http.server 8000` in the project directory and open `http://localhost:8000`.

## Demonstration flow
1. **Discover:** Start on the personalized home screen. The recommendation cards show why each title was selected.
2. **Recommendation modes:** Switch between `For you`, `Because you liked it`, and `Popular`.
3. **Search:** Search by title, genre, actor, or director in the catalog field.
4. **Rate:** Select any movie, open its detail panel, then choose `Loved it` or `Liked it`. The movie is added to the personal library.
5. **Library:** Select `My library` to see rated and saved titles. Use the detail panel to remove a title.
6. **Graph explorer:** Select `Graph explorer`. The canvas shows the user at the center, connected movies, and shared genre/director features. Reset with the circular arrow.

## Neo4j demonstration
Open Neo4j Browser, execute `database/schema.cypher`, then `database/seed.cypher`. Run individual examples from `database/queries.cypher`, replacing `$userId` with `u1`, `$movieId` with `m1`, and `$limit` with `5`.

## Suggested final demo script
Show the problem and graph schema, browse the seeded graph, run the collaborative query, explain the returned recommendation path, run shortest path, show the responsive UI, then show constraints/indexes and the report's rubric mapping.
