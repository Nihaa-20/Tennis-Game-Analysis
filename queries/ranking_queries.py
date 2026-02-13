def get_ranking_query(option):

    queries = {

        "Q1 - All competitors with rank": """
            SELECT co.competitor_name, co.country, cr.rank, cr.points,
                   cr.competitions_played, cr.ranking_name,
                   cr.year, cr.week
            FROM Competitor_Rankings cr
            JOIN Competitors co
                ON cr.competitor_id = co.competitor_id
            ORDER BY cr.rank
        """,

        "Q2 - Top 5 ranked players": """
            SELECT co.competitor_name, co.country, cr.rank, cr.points
            FROM Competitor_Rankings cr
            JOIN Competitors co
                ON cr.competitor_id = co.competitor_id
            WHERE cr.rank <= 5
            ORDER BY cr.rank
        """,

        "Q3 - Stable rank players": """
            SELECT co.competitor_name, co.country, cr.rank,
                   cr.points, cr.movement
            FROM Competitor_Rankings cr
            JOIN Competitors co
                ON cr.competitor_id = co.competitor_id
            WHERE cr.movement = 0
            ORDER BY cr.rank
        """,

        "Q4 - Total points from Croatia": """
            SELECT co.country, SUM(cr.points) AS total_points
            FROM Competitor_Rankings cr
            JOIN Competitors co
                ON cr.competitor_id = co.competitor_id
            WHERE co.country = 'Croatia'
            GROUP BY co.country
        """,

        "Q5 - Competitors per country": """
            SELECT co.country,
                   COUNT(co.competitor_id) AS total_competitors
            FROM Competitors co
            JOIN Competitor_Rankings cr
                ON cr.competitor_id = co.competitor_id
            GROUP BY co.country
            ORDER BY total_competitors DESC
        """,

        "Q6 - Highest points in current week": """
            SELECT TOP 10 co.competitor_name,
                   co.country,
                   cr.rank,
                   cr.points,
                   cr.week,
                   cr.year
            FROM Competitor_Rankings cr
            JOIN Competitors co
                ON cr.competitor_id = co.competitor_id
            WHERE cr.year = (SELECT MAX(year) FROM Competitor_Rankings)
            AND cr.week = (
                SELECT MAX(week)
                FROM Competitor_Rankings
                WHERE year = (SELECT MAX(year) FROM Competitor_Rankings)
            )
            ORDER BY cr.points DESC
        """
    }

    return queries.get(option)
