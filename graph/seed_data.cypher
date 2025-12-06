// --- Genres ---
CREATE (g1:Genre {genre_id: "g1", name: "Sci-Fi"});
CREATE (g2:Genre {genre_id: "g2", name: "Action"});
CREATE (g3:Genre {genre_id: "g3", name: "Drama"});

// --- Persons ---
CREATE (p1:Person {person_id: "p1", name: "Christopher Nolan"});
CREATE (p2:Person {person_id: "p2", name: "Leonardo DiCaprio"});
CREATE (p3:Person {person_id: "p3", name: "Joseph Gordon-Levitt"});
CREATE (p4:Person {person_id: "p4", name: "Matthew McConaughey"});

// --- Movies ---
CREATE (m1:Movie {
    movie_id: "m1",
    title: "Inception",
    year: 2010,
    description: "A thief uses dream-sharing technology to steal secrets from targets."
});

CREATE (m2:Movie {
    movie_id: "m2",
    title: "Interstellar",
    year: 2014,
    description: "A team of explorers travel through a wormhole in search of a new home."
});

CREATE (m3:Movie {
    movie_id: "m3",
    title: "The Dark Knight",
    year: 2008,
    description: "Batman faces the Joker in a battle for Gotham's soul."
});

// --- Relationships ---

// Inception
MATCH (p1:Person {name: "Christopher Nolan"}), (m1:Movie {title: "Inception"})
CREATE (p1)-[:DIRECTED]->(m1);

MATCH (p2:Person {name: "Leonardo DiCaprio"}), (m1:Movie {title: "Inception"})
CREATE (p2)-[:ACTED_IN]->(m1);

MATCH (p3:Person {name: "Joseph Gordon-Levitt"}), (m1:Movie {title: "Inception"})
CREATE (p3)-[:ACTED_IN]->(m1);

MATCH (g1:Genre {name: "Sci-Fi"}), (m1:Movie {title: "Inception"})
CREATE (m1)-[:HAS_GENRE]->(g1);

// Interstellar
MATCH (p1:Person {name: "Christopher Nolan"}), (m2:Movie {title: "Interstellar"})
CREATE (p1)-[:DIRECTED]->(m2);

MATCH (p4:Person {name: "Matthew McConaughey"}), (m2:Movie {title: "Interstellar"})
CREATE (p4)-[:ACTED_IN]->(m2);

MATCH (g1:Genre {name: "Sci-Fi"}), (m2:Movie {title: "Interstellar"})
CREATE (m2)-[:HAS_GENRE]->(g1);

// The Dark Knight
MATCH (p1:Person {name: "Christopher Nolan"}), (m3:Movie {title: "The Dark Knight"})
CREATE (p1)-[:DIRECTED]->(m3);

MATCH (p2:Person {name: "Leonardo DiCaprio"}), (m3:Movie {title: "The Dark Knight"})
CREATE (p2)-[:ACTED_IN]->(m3);

MATCH (g2:Genre {name: "Action"}), (m3:Movie {title: "The Dark Knight"})
CREATE (m3)-[:HAS_GENRE]->(g2);
