def get_competition_query(option):

    queries = {

        "Q1 - List all competitions": """
            SELECT competition_name, type, gender, category_name
            FROM Competitions
            ORDER BY category_name, competition_name
        """,

        "Q2 - Count competitions per category": """
            SELECT category_name, COUNT(*) AS total_competitions
            FROM Competitions
            GROUP BY category_name
            ORDER BY total_competitions DESC
        """,

        "Q3 - Competitions of type doubles": """
            SELECT competition_name, gender, category_name
            FROM Competitions
            WHERE type = 'doubles'
            ORDER BY competition_name
        """,

        "Q4 - Competitions in ITF Men": """
            SELECT competition_name, type, gender
            FROM Competitions
            WHERE category_name = 'ITF Men'
            ORDER BY competition_name
        """,

        "Q5 - Parent and sub competitions": """
            SELECT 
            parent.competition_id AS parent_id,
            parent.competition_name AS parent_competition,
            child.competition_id AS sub_id,
            child.competition_name AS sub_competition,
            child.type,
            child.gender,
            child.category_name
            FROM Competitions child
            INNER JOIN Competitions parent
                ON child.parent_id = parent.competition_id
            ORDER BY parent.competition_name, child.competition_name;
        """,

        "Q6 - Distribution by category & type": """
            SELECT category_name,
                   type AS competition_type,
                   COUNT(*) AS total_competitions
            FROM Competitions
            GROUP BY category_name, type
            ORDER BY category_name, total_competitions DESC
        """,

        "Q7 - Top-level competitions": """
            SELECT competition_name, type, gender, category_name
            FROM Competitions
            WHERE parent_id IS NULL
            ORDER BY competition_name
        """
    }

    return queries.get(option)
