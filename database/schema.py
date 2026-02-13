from .db_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

print("✅ Connected to tennis_db.sqlite for schema creation")

# -----------------------------
# Categories
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Categories (
    category_id TEXT PRIMARY KEY,
    category_name TEXT NOT NULL
)
""")

# -----------------------------
# Competitions
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Competitions (
    competition_id TEXT PRIMARY KEY,
    competition_name TEXT NOT NULL,
    parent_id TEXT,
    type TEXT,
    gender TEXT,
    category_id TEXT,
    category_name TEXT,
    FOREIGN KEY(category_id) REFERENCES Categories(category_id)
)
""")

# -----------------------------
# Complexes
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Complexes (
    complex_id TEXT PRIMARY KEY,
    complex_name TEXT NOT NULL
)
""")

# -----------------------------
# Venues
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Venues (
    venue_id TEXT PRIMARY KEY,
    venue_name TEXT NOT NULL,
    city_name TEXT NOT NULL,
    country_name TEXT NOT NULL,
    country_code TEXT NOT NULL,
    timezone TEXT NOT NULL,
    complex_id TEXT,
    FOREIGN KEY(complex_id) REFERENCES Complexes(complex_id)
)
""")

# -----------------------------
# Competitors
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Competitors (
    competitor_id TEXT PRIMARY KEY,
    competitor_name TEXT,
    country TEXT,
    country_code TEXT,
    abbreviation TEXT
)
""")

# -----------------------------
# Competitor Rankings
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS Competitor_Rankings (
    competitor_id TEXT,
    rank INTEGER,
    movement INTEGER,
    points INTEGER,
    competitions_played INTEGER,
    type_id INTEGER,
    ranking_name TEXT,
    year INTEGER,
    week INTEGER,
    gender TEXT,
    PRIMARY KEY (competitor_id, type_id, year, week),
    FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
)
""")

conn.commit()
cursor.close()
conn.close()
print("✅ All tables created successfully!")
