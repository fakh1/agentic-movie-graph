// --- Constraints ---
CREATE CONSTRAINT movie_id_unique IF NOT EXISTS
FOR (m:Movie) REQUIRE m.movie_id IS UNIQUE;

CREATE CONSTRAINT person_id_unique IF NOT EXISTS
FOR (p:Person) REQUIRE p.person_id IS UNIQUE;

CREATE CONSTRAINT genre_id_unique IF NOT EXISTS
FOR (g:Genre) REQUIRE g.genre_id IS UNIQUE;

// --- Indexes (optional but helps queries) ---
CREATE INDEX movie_title_index IF NOT EXISTS
FOR (m:Movie) ON (m.title);

CREATE INDEX person_name_index IF NOT EXISTS
FOR (p:Person) ON (p.name);

CREATE INDEX genre_name_index IF NOT EXISTS
FOR (g:Genre) ON (g.name);
