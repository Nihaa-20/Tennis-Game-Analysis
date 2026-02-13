def get_venue_query(option):

    queries = {
        "Q1 - Venues with complex name": """
            SELECT v.venue_name, c.complex_name
            FROM Venues v
            JOIN Complexes c ON v.complex_id = c.complex_id
        """,

        "Q2 - Count venues per complex": """
            SELECT c.complex_name, COUNT(v.venue_id) AS total_venues
            FROM Venues v
            JOIN Complexes c ON v.complex_id = c.complex_id
            GROUP BY c.complex_name
        """,

        "Q3 - Venues in Chile": """
            SELECT venue_name, city_name, country_name
            FROM Venues
            WHERE country_name = 'Chile'
        """,

        "Q4 - All venues and timezones": """
            SELECT venue_name, city_name, country_name, timezone
            FROM Venues
        """,

        "Q5 - Complexes with >1 venue": """
            SELECT c.complex_name, COUNT(v.venue_id) AS venue_count
            FROM Venues v
            JOIN Complexes c ON v.complex_id = c.complex_id
            GROUP BY c.complex_name
            HAVING COUNT(v.venue_id) > 1
        """,

        "Q6 - Venues grouped by country": """
            SELECT country_name, COUNT(*) AS total_venues
            FROM Venues
            GROUP BY country_name
        """,

        "Q7 - Venues for Nacional complex": """
            SELECT v.venue_name, c.complex_name
            FROM Venues v
            JOIN Complexes c ON v.complex_id = c.complex_id
            WHERE c.complex_name = 'Nacional'
        """
    }

    return queries.get(option)
