import json
from database.db_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

print("✅ Connected to tennis_db.sqlite for data insertion")

# -----------------------------
# Load JSON
# -----------------------------
with open("data/raw/competitions.json", "r", encoding="utf-8") as f:
    competitions_data = json.load(f)

with open("data/raw/complexes.json", "r", encoding="utf-8") as f:
    complexes_data = json.load(f)

with open("data/raw/double_rankings.json", "r", encoding="utf-8") as f:
    rankings_data = json.load(f)

# -----------------------------
# Insert Categories & Competitions
# -----------------------------
for comp in competitions_data["competitions"]:
    cat_id = comp["category"]["id"]
    cat_name = comp["category"]["name"]

    # SQLite: INSERT OR IGNORE
    cursor.execute("""
        INSERT OR IGNORE INTO Categories (category_id, category_name)
        VALUES (?, ?)
    """, (cat_id, cat_name))

    cursor.execute("""
        INSERT OR IGNORE INTO Competitions (
            competition_id,
            competition_name,
            parent_id,
            type,
            gender,
            category_id,
            category_name
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (comp["id"],
         comp["name"],
         comp.get("parent_id"),   # parent_id can be NULL
         comp.get("type"),
         comp.get("gender", "unknown"),
         cat_id,
         cat_name)
    )

conn.commit()
print("✅ Competitions inserted")

# -----------------------------
# Insert Complexes & Venues
# -----------------------------
for complex_ in complexes_data["complexes"]:
    cursor.execute("""
        INSERT OR IGNORE INTO Complexes (complex_id, complex_name)
        VALUES (?, ?)
    """, (complex_["id"], complex_["name"]))

    for venue in complex_.get("venues", []):
        cursor.execute("""
            INSERT OR IGNORE INTO Venues (
                venue_id, venue_name, city_name,
                country_name, country_code, timezone, complex_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (venue["id"],
             venue["name"],
             venue["city_name"],
             venue["country_name"],
             venue["country_code"],
             venue["timezone"],
             complex_["id"])
        )

conn.commit()
print("✅ Complexes and Venues inserted")

# -----------------------------
# Insert Competitors & Rankings
# -----------------------------
for ranking_block in rankings_data["rankings"]:
    for comp_rank in ranking_block["competitor_rankings"]:
        competitor = comp_rank["competitor"]

        cursor.execute("""
            INSERT OR IGNORE INTO Competitors (
                competitor_id, competitor_name,
                country, country_code, abbreviation
            )
            VALUES (?, ?, ?, ?, ?)
        """,
            (competitor["id"],
             competitor.get("name"),
             competitor.get("country"),
             competitor.get("country_code"),
             competitor.get("abbreviation"))
        )

        cursor.execute("""
            INSERT INTO Competitor_Rankings (
                competitor_id, rank, movement, points,
                competitions_played, type_id,
                ranking_name, year, week, gender
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (competitor["id"],
             comp_rank["rank"],
             comp_rank["movement"],
             comp_rank["points"],
             comp_rank["competitions_played"],
             ranking_block["type_id"],
             ranking_block["name"],
             ranking_block["year"],
             ranking_block["week"],
             ranking_block["gender"])
        )

conn.commit()
cursor.close()
conn.close()
print("✅ All data inserted into SQLite and connection closed!")
