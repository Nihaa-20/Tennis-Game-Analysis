import streamlit as st
import pandas as pd
import sys
import os
import plotly.express as px
from queries.competition_queries import get_competition_query
from queries.venue_queries import get_venue_query
from queries.ranking_queries import get_ranking_query

# ------------------ PATH FIX ------------------
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from database.db_connection import get_connection

conn = get_connection()

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Tennis Game Analytics",
    page_icon="🎾",
    layout="wide"
)

# -------------------- HEADER --------------------
st.markdown('<h1 style="text-align:center;">🎾 Tennis Game Analytics Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align:center; color: #666;">Competition • Venue • Player Insights</h3>', unsafe_allow_html=True)

# =========================
# MAIN BACKGROUND COLOR
# =========================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #d8e8f7;
}
[data-testid="stSidebar"] {
    background-color: #aac1d8;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TABS STYLE
# =========================
st.markdown("""
<style>
.stTabs [data-baseweb="tab-list"] {
    justify-content: center;
    gap: 50px;
}

.stTabs [data-baseweb="tab"] {
    font-size: 24px;
    font-weight: bold;
    padding: 12px 25px;
}

.stTabs [aria-selected="true"] {
    border-bottom: 4px solid black;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# KPI CARD CSS (Add Once)
# -------------------------------------------------
st.markdown("""
    <style>
    .kpi-card {
        background: linear-gradient(135deg, #1f2937, #111827);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
    }
    .kpi-title {
        color: #9ca3af;
        font-size: 16px;
        font-weight: 500;
    }
    .kpi-value {
        color: white;
        font-size: 28px;
        font-weight: bold;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# 🌍 GLOBAL SIDEBAR FILTERS (ALL FILTERS MOVED HERE)
# =====================================================
with st.sidebar:

    st.markdown("## 🌍 Global Filters")

    # ---------------- YEAR ----------------
    year_list = pd.read_sql(
        "SELECT DISTINCT year FROM Competitor_Rankings ORDER BY year DESC",
        conn
    )['year'].tolist()
    selected_year = st.selectbox("Season / Year", year_list)

    # ---------------- COUNTRY ----------------
    countries = pd.read_sql(
        "SELECT DISTINCT country FROM Competitors ORDER BY country",
        conn
    )['country'].tolist()
    countries = ["All"] + countries
    selected_country = st.selectbox("Country", countries)

    # ---------------- GENDER ----------------
    gender_list = pd.read_sql(
        "SELECT DISTINCT gender FROM Competitions WHERE gender IS NOT NULL ORDER BY gender",
        conn
    )['gender'].tolist()
    gender_list = ["All"] + gender_list
    selected_gender = st.selectbox("Gender", gender_list)


    st.markdown("---")
    st.markdown("## 🏆 Competition Filters")

    categories = pd.read_sql(
        "SELECT DISTINCT category_name FROM Categories ORDER BY category_name",
        conn
    )['category_name'].tolist()
    categories = ["All"] + categories
    selected_category = st.selectbox("Category", categories)

    competitions = pd.read_sql(
        "SELECT DISTINCT competition_name FROM Competitions ORDER BY competition_name",
        conn
    )['competition_name'].tolist()
    competitions = ["All"] + competitions
    selected_competition = st.selectbox("Competition", competitions)

    selected_type = st.selectbox("Type", ["All", "singles", "doubles", "mixed", "mixed_doubles"])

    st.markdown("---")
    st.markdown("## 📍 Venue Filters")

    cities = pd.read_sql(
        "SELECT DISTINCT city_name FROM Venues ORDER BY city_name",
        conn
    )['city_name'].tolist()
    cities = ["All"] + cities
    selected_city = st.selectbox("City", cities)

    complexes = pd.read_sql(
        "SELECT DISTINCT complex_name FROM Complexes ORDER BY complex_name",
        conn
    )['complex_name'].tolist()
    complexes = ["All"] + complexes
    selected_complex = st.selectbox("Complex", complexes)

    venues = pd.read_sql(
        "SELECT DISTINCT venue_name FROM Venues ORDER BY venue_name",
        conn
    )['venue_name'].tolist()
    venues = ["All"] + venues
    selected_venue = st.selectbox("Venue", venues)

    st.markdown("---")
    st.markdown("## 👤 Player Filters")

    rank_range = st.slider("Rank Range", 1, 500, (1, 100))

    competitor_list = pd.read_sql(
        "SELECT DISTINCT competitor_name FROM Competitors ORDER BY competitor_name",
        conn
    )['competitor_name'].tolist()
    competitor_list = ["All"] + competitor_list
    selected_competitor = st.selectbox("Competitor", competitor_list)

# =========================
# MAIN TABS
# =========================
tab1, tab2, tab3 = st.tabs(["🏆 Competition", "📍 Venue", "👤 Player"])

# =====================================================
# TAB 1: COMPETITION
# =====================================================
with tab1:

    # =====================================================
    # 🔹 SECTION 2: Key Metrics
    # =====================================================
    st.subheader("Key Metrics")
    k1, k2, k3, k4 = st.columns(4)

    total_comp = pd.read_sql("SELECT COUNT(*) as total FROM Competitions", conn).iloc[0]['total']
    total_categories = pd.read_sql("SELECT COUNT(DISTINCT category_name) as total FROM Competitions", conn).iloc[0]['total']
    singles_events = pd.read_sql("SELECT COUNT(*) as total FROM Competitions WHERE type='singles'", conn).iloc[0]['total']
    doubles_events = pd.read_sql("SELECT COUNT(*) as total FROM Competitions WHERE type='doubles'", conn).iloc[0]['total']

    k1.markdown(f'<div class="kpi-card"><div class="kpi-title">Total Competitions</div><div class="kpi-value">{total_comp}</div></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi-card"><div class="kpi-title">Categories</div><div class="kpi-value">{total_categories}</div></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="kpi-card"><div class="kpi-title">Singles Events</div><div class="kpi-value">{singles_events}</div></div>', unsafe_allow_html=True)
    k4.markdown(f'<div class="kpi-card"><div class="kpi-title">Doubles Events</div><div class="kpi-value">{doubles_events}</div></div>', unsafe_allow_html=True)

    st.divider()

    # =====================================================
    # 🔹 Filtered Competition Table 
    # =====================================================
    competition_full = pd.read_sql("""
    SELECT competition_name,
           category_name,
           type,
           gender,
           parent_id
    FROM Competitions
    """, conn)

    visual_competition = competition_full.copy()

    if selected_category != "All":
        visual_competition = visual_competition[visual_competition['category_name'] == selected_category]
    
    if selected_competition != "All":
        visual_competition = visual_competition[visual_competition['competition_name'] == selected_competition]

    if selected_type != "All":
        visual_competition = visual_competition[visual_competition['type'] == selected_type]

    if selected_gender != "All":
        visual_competition = visual_competition[visual_competition['gender'] == selected_gender]

    st.subheader("🔹 Filtered Competition Table")
    st.dataframe(
        visual_competition[['competition_name','category_name','type','gender','parent_id']],
        use_container_width=True
    )

    # =====================================================
    # 🔹 SECTION 3: Competition Queries
    # =====================================================
    st.subheader("📋 Competition Queries")
    comp_options = [
        "Q1 - List all competitions",
        "Q2 - Count competitions per category",
        "Q3 - Competitions of type doubles",
        "Q4 - Competitions in ITF Men",
        "Q5 - Parent and sub competitions",
        "Q6 - Distribution by category & type",
        "Q7 - Top-level competitions"
    ]
    comp_selected = st.selectbox("Select Query", comp_options, key="comp_query")
    comp_query = get_competition_query(comp_selected)
    comp_df = pd.read_sql(comp_query, conn)
    st.dataframe(comp_df, use_container_width=True)

    st.divider()

    # =====================================================
    # 🔹 SECTION 4: Visual Analytics
    # =====================================================
    st.subheader("📈 Visual Analytics")

    visual_filters = ["1=1"]
    if selected_category != "All":
        visual_filters.append(f"category_name = '{selected_category}'")
    if selected_competition != "All":
        visual_filters.append(f"competition_name = '{selected_competition}'")
    if selected_type != "All":
        visual_filters.append(f"type = '{selected_type}'")
    if selected_gender != "All":
        visual_filters.append(f"gender = '{selected_gender}'")

    filter_sql = " AND ".join(visual_filters)

    # Competitions by Category
    comp_by_category = pd.read_sql(
        f"""
        SELECT category_name, competition_name, type, gender, COUNT(*) as total
        FROM Competitions
        WHERE {filter_sql}
        GROUP BY category_name, competition_name, type, gender
        """,
        conn
    ).sort_values('total', ascending=False)

    st.write("### Competitions by Category (Table)")
    st.dataframe(
        comp_by_category.style.applymap(lambda v: 'background-color: lightblue', subset=['category_name']),
        use_container_width=True
    )

    fig_cat = px.bar(
        comp_by_category.groupby('category_name', as_index=False).sum().sort_values('total', ascending=False),
        x='category_name', y='total', text='total',
        title='Competitions by Category'
    )
    fig_cat.update_layout(xaxis_tickangle=-45, height=400, margin=dict(l=20, r=20, t=50, b=150))
    st.plotly_chart(fig_cat, use_container_width=True)

    # Competitions by Type
    comp_by_type = pd.read_sql(
        f"""
        SELECT type, competition_name, category_name, gender, COUNT(*) as total
        FROM Competitions
        WHERE {filter_sql}
        GROUP BY type, competition_name, category_name, gender
        """,
        conn
    ).sort_values('total', ascending=False)

    st.write("### Competitions by Type (Table)")
    st.dataframe(
        comp_by_type.style.applymap(lambda v: 'background-color: lightblue', subset=['type']),
        use_container_width=True
    )

    fig_type = px.bar(
        comp_by_type.groupby('type', as_index=False).sum().sort_values('total', ascending=False),
        x='type', y='total', text='total',
        title='Competitions by Type'
    )
    fig_type.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=50))
    st.plotly_chart(fig_type, use_container_width=True)

    # Competitions by Gender
    comp_by_gender = pd.read_sql(
        f"""
        SELECT gender, competition_name, type, category_name, COUNT(*) as total
        FROM Competitions
        WHERE {filter_sql} AND gender IS NOT NULL AND gender != ''
        GROUP BY gender, competition_name, type, category_name
        """,
        conn
    ).sort_values('total', ascending=False)

    st.write("### Competitions by Gender (Table)")
    st.dataframe(
        comp_by_gender.style.applymap(lambda v: 'background-color: lightblue', subset=['gender']),
        use_container_width=True
    )

    fig_gender = px.bar(
        comp_by_gender.groupby('gender', as_index=False).sum().sort_values('total', ascending=False),
        x='gender', y='total', text='total',
        title='Competitions by Gender'
    )
    fig_gender.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=50))
    st.plotly_chart(fig_gender, use_container_width=True)

# =====================================================
# TAB 2: Venue & Complexes
# =====================================================
with tab2:

    # =====================================================
    # -------- KPI --------
    # =====================================================
    st.subheader("Key Metrics")
    k1, k2, k3, k4 = st.columns(4)

    total_complexes = pd.read_sql("SELECT COUNT(*) as total FROM Complexes", conn).iloc[0]['total']
    total_venues = pd.read_sql("SELECT COUNT(*) as total FROM Venues", conn).iloc[0]['total']
    total_countries = pd.read_sql("SELECT COUNT(DISTINCT country_name) as total FROM Venues", conn).iloc[0]['total']
    total_cities = pd.read_sql("SELECT COUNT(DISTINCT city_name) as total FROM Venues", conn).iloc[0]['total']

    k1.markdown(f'<div class="kpi-card"><div class="kpi-title">Complexes</div><div class="kpi-value">{total_complexes}</div></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi-card"><div class="kpi-title">Venues</div><div class="kpi-value">{total_venues}</div></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="kpi-card"><div class="kpi-title">Countries</div><div class="kpi-value">{total_countries}</div></div>', unsafe_allow_html=True)
    k4.markdown(f'<div class="kpi-card"><div class="kpi-title">Cities</div><div class="kpi-value">{total_cities}</div></div>', unsafe_allow_html=True)

    st.divider()

    # =====================================================
    # 🔹 Filtered Venue & Complex Table
    # =====================================================
    venue_full = pd.read_sql("""
        SELECT 
            v.venue_name,
            v.city_name,
            v.country_name,
            c.complex_name,
            v.timezone
        FROM Venues v
        LEFT JOIN Complexes c
            ON v.complex_id = c.complex_id
    """, conn)

    visual_venue_master = venue_full.copy()

    if selected_city != "All":
        visual_venue_master = visual_venue_master[visual_venue_master['city_name'] == selected_city]
    if selected_complex != "All":
        visual_venue_master = visual_venue_master[visual_venue_master['complex_name'] == selected_complex]
    if selected_venue != "All":
        visual_venue_master = visual_venue_master[visual_venue_master['venue_name'] == selected_venue]

    st.subheader("🔹 Filtered Venue & Complex Table")
    st.dataframe(
        visual_venue_master[['venue_name','city_name','country_name','complex_name','timezone']],
        use_container_width=True
    )

    # =====================================================
    # 🔹 ORIGINAL SQL QUERIES (Venue Queries)
    # =====================================================
    st.subheader("Venue Queries")
    venue_options = [
        "Q1 - Venues with complex name",
        "Q2 - Count venues per complex",
        "Q3 - Venues in Chile",
        "Q4 - All venues and timezones",
        "Q5 - Complexes with >1 venue",
        "Q6 - Venues grouped by country",
        "Q7 - Venues for Nacional complex"
    ]
    venue_selected = st.selectbox("Select Query", venue_options, key="venue_query")
    venue_query = get_venue_query(venue_selected)
    venue_df = pd.read_sql(venue_query, conn)
    st.dataframe(venue_df)

    st.divider()
    
    # =====================================================
    # 🔹 SECTION 1: Complex Overview
    # =====================================================
    complex_overview = pd.read_sql("""
        SELECT c.complex_name, COUNT(v.venue_id) as total_venues,
               v.venue_name, v.city_name
        FROM Complexes c
        LEFT JOIN Venues v ON c.complex_id = v.complex_id
        GROUP BY c.complex_name, v.venue_name, v.city_name
        ORDER BY total_venues DESC
    """, conn)

    visual_complex = complex_overview.copy()
    if selected_complex != "All":
        visual_complex = visual_complex[visual_complex['complex_name'] == selected_complex]
    if selected_city != "All":
        visual_complex = visual_complex[visual_complex['city_name'] == selected_city]
    if selected_venue != "All":
        visual_complex = visual_complex[visual_complex['venue_name'] == selected_venue]

    st.subheader("🔹 Complex Overview")
    st.dataframe(
        visual_complex[['complex_name','venue_name','city_name','total_venues']].style.applymap(
            lambda v: 'background-color: lightblue' if v else '', subset=['complex_name']
        ),
        use_container_width=True
    )

    fig_complex = px.bar(
        visual_complex.groupby('complex_name', as_index=False)['total_venues'].sum().sort_values('total_venues', ascending=False),
        x='complex_name',
        y='total_venues',
        text='total_venues',
        title='Number of Venues per Complex'
    )
    fig_complex.update_layout(xaxis_tickangle=-45, height=400, margin=dict(l=20, r=20, t=50, b=150))
    st.plotly_chart(fig_complex, use_container_width=True)

    # =====================================================
    # 🔹 SECTION 2: Venue Details
    # =====================================================
    venue_details = pd.read_sql("""
        SELECT v.venue_name, v.city_name, v.country_name, v.timezone, c.complex_name
        FROM Venues v
        LEFT JOIN Complexes c ON v.complex_id = c.complex_id
        ORDER BY v.venue_name
    """, conn)

    visual_venue = venue_details.copy()
    if selected_city != "All":
        visual_venue = visual_venue[visual_venue['city_name'] == selected_city]
    if selected_complex != "All":
        visual_venue = visual_venue[visual_venue['complex_name'] == selected_complex]
    if selected_venue != "All":
        visual_venue = visual_venue[visual_venue['venue_name'] == selected_venue]

    st.subheader("🔹 Venue Details")
    st.dataframe(
        visual_venue[['venue_name','city_name','complex_name','country_name','timezone']].style.applymap(
            lambda v: 'background-color: lightblue' if v else '', subset=['venue_name','city_name']
        ),
        use_container_width=True
    )

    fig_venue = px.bar(
        visual_venue.groupby('city_name', as_index=False)['venue_name'].count().sort_values('venue_name', ascending=False),
        x='city_name',
        y='venue_name',
        text='venue_name',
        title='Number of Venues per City'
    )
    fig_venue.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=150))
    st.plotly_chart(fig_venue, use_container_width=True)

    # =====================================================
    # 🔹 SECTION 3: Country Distribution
    # =====================================================
    visual_country = visual_venue.copy()

    st.subheader("🔹 Country Distribution")
    st.dataframe(
        visual_country[['country_name','venue_name','city_name','complex_name','timezone']].style.applymap(
            lambda v: 'background-color: lightblue' if v else '', subset=['country_name']
        ),
        use_container_width=True
    )

    fig_country = px.bar(
        visual_country.groupby('country_name', as_index=False)['venue_name'].count().sort_values('venue_name', ascending=False),
        x='country_name',
        y='venue_name',
        text='venue_name',
        title='Number of Venues per Country'
    )
    fig_country.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=150))
    st.plotly_chart(fig_country, use_container_width=True)

# =====================================================
# TAB 3: PLAYER RANKINGS
# =====================================================
with tab3:

    # -------------------------------------------------
    # LOAD FULL DATA (FOR KPI ONLY)
    # -------------------------------------------------
    full_player_df = pd.read_sql(
        """
        SELECT r.competitor_id, c.competitor_name, c.country,
               r.rank, r.movement, r.points,
               r.competitions_played, r.type_id,
               r.ranking_name, r.year, r.week, r.gender
        FROM Competitor_Rankings r
        LEFT JOIN Competitors c
        ON r.competitor_id = c.competitor_id
        """,
        conn
    )

    # -------------------------------------------------
    # APPLY YOUR ORIGINAL FILTERS (ONLY FOR VISUALS)
    # -------------------------------------------------
    visual_player = full_player_df.copy()

    # Rank range filter
    visual_player = visual_player[
        (visual_player['rank'] >= rank_range[0]) &
        (visual_player['rank'] <= rank_range[1])
    ]

    # Competitor filter
    if selected_competitor != "All":
        visual_player = visual_player[
            visual_player['competitor_name'] == selected_competitor
        ]

    # -------------------------------------------------
    # KPI SECTION (STABLE - Uses FULL DATA)
    # -------------------------------------------------
    st.subheader("Key Metrics")

    k1, k2, k3, k4 = st.columns(4)

    total_players = full_player_df['competitor_id'].nunique()
    highest_points = full_player_df['points'].max()
    lowest_rank = full_player_df['rank'].max()
    avg_points = int(full_player_df['points'].mean() or 0)

    k1.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Players</div>
        <div class="kpi-value">{total_players}</div>
    </div>
    """, unsafe_allow_html=True)

    k2.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Highest Points</div>
        <div class="kpi-value">{highest_points}</div>
    </div>
    """, unsafe_allow_html=True)

    k3.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Lowest Rank</div>
        <div class="kpi-value">{lowest_rank}</div>
    </div>
    """, unsafe_allow_html=True)

    k4.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Average Points</div>
        <div class="kpi-value">{avg_points}</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # -------------------------------------------------
    # SQL Queries Section
    # -------------------------------------------------
    st.subheader("Ranking Queries")

    rank_options = [
        "Q1 - All competitors with rank",
        "Q2 - Top 5 ranked players",
        "Q3 - Stable rank players",
        "Q4 - Total points from Croatia",
        "Q5 - Competitors per country",
        "Q6 - Highest points in current week"
    ]

    rank_selected = st.selectbox("Select Query", rank_options, key="rank_query")
    rank_query = get_ranking_query(rank_selected)

    rank_df = pd.read_sql(rank_query, conn)
    st.dataframe(rank_df, use_container_width=True)

    st.divider()

    # -------------------------------------------------
    # FILTERED RANKING TABLE
    # -------------------------------------------------
    st.subheader("Filtered Ranking Table")

    st.dataframe(
        visual_player[
            ['rank','competitor_name','country',
             'points','movement','year','week']
        ],
        use_container_width=True
    )

    # -------------------------------------------------
    # TOP 10 PLAYERS
    # -------------------------------------------------
    st.subheader("Top 10 Players")

    top10_choice = st.radio(
        "Top 10 by:",
        ["Rank", "Points"],
        horizontal=True
    )

    if top10_choice == "Rank":
        top10_df = visual_player.nsmallest(10, 'rank')
    else:
        top10_df = visual_player.nlargest(10, 'points')

    st.dataframe(
        top10_df[
            ['rank','competitor_name','country',
             'points','movement','year','week']
        ],
        use_container_width=True
    )

    # -------------------------------------------------
    # MOVEMENT ANALYSIS
    # -------------------------------------------------
    st.subheader("Movement Analysis")

    def categorize_movement(x):
        if x > 0:
            return "Improved"
        elif x < 0:
            return "Dropped"
        else:
            return "Unchanged"

    movement_df = visual_player.copy()
    movement_df['Movement'] = movement_df['movement'].apply(categorize_movement)

    movement_counts = (
        movement_df['Movement']
        .value_counts()
        .reindex(["Dropped", "Unchanged", "Improved"])
        .fillna(0)
    )

    movement_chart_df = movement_counts.reset_index()
    movement_chart_df.columns = ['Movement', 'Count']

    fig_movement = px.pie(
        movement_chart_df,
        names='Movement',
        values='Count',
        color='Movement',
        color_discrete_map={
            "Improved": "green",
            "Dropped": "red",
            "Unchanged": "gray"
        },
        title="Player Movement Distribution"
    )

    fig_movement.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig_movement, use_container_width=True)
