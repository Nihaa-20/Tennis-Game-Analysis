# 🎾 Game Analytics: Unlocking Tennis Data with SportRadar API

**End-to-End Tennis Data Engineering & Analytics Dashboard**  
Built with Python, SQL Server & Streamlit

---

## 📌 Executive Summary
This project is a full-stack data analytics solution that integrates the SportRadar API with a relational database and an interactive Streamlit dashboard to analyze tennis competitions, venues, and player rankings.

The system demonstrates:
- API data ingestion
- Relational database design
- SQL-based analytical querying
- Data transformation using Pandas
- Interactive dashboard visualization
- Dynamic filtering with real-time updates

It follows a modular architecture separating API, database, query logic, and presentation layers.

---

## 🏗️ System Architecture
```
SportRadar API
      │
      ▼
JSON Extraction Layer (api/)
      │
      ▼
Data Processing & Cleaning (scripts/)
      │
      ▼
SQL Server Database (Normalized Schema)
      │
      ▼
Query Layer (queries/)
      │
      ▼
Streamlit Analytics Dashboard (app.py)
```
---

## 🧱 Database Design
The database is designed using normalized relational principles.

### 🧱 Core Tables

| Table Name            | Description                         |
|-----------------------|-------------------------------------|
| Categories            | Stores competition categories       |
| Competitions          | Tournament-level details            |
| Complexes             | Tennis complexes information        |
| Venues                | Individual playing venues           |
| Competitors           | Player profile information          |
| Competitor_Rankings   | Weekly player ranking statistics    |


### Key Design Decisions
- Composite Primary Key on `Competitor_Rankings`:
  `(competitor_id, type_id, year, week)`
- Foreign key relationships between competitions, venues, and competitors
- Structured for analytical querying (grouping, filtering, aggregation)

---

## 📊 Dashboard Modules

### 🏆 Competition Analytics
- Total competitions KPI
- Category distribution
- Type distribution (Singles / Doubles)
- Gender-based breakdown
- Parent & sub-competition mapping
- SQL-driven dynamic queries

### 📍 Venue & Complex Analytics
- Complex-to-venue relationship mapping
- Venue distribution by city and country
- Country-wise venue count visualization
- Timezone insights
- Interactive filtering

### 👤 Player Ranking Analytics
- Rank range filtering (1–500)
- Competitor-specific drill-down
- Country-based filtering

**KPI Metrics:**
- Total Players
- Highest Points
- Lowest Rank
- Average Points

**Additional Insights:**
- Top 10 by Rank
- Top 10 by Points
- Movement classification (Improved, Dropped, Unchanged)

---

## 🎛️ Dynamic Filtering System
The dashboard supports global filtering across modules:
- Year / Season
- Country
- Gender
- Category
- Competition
- City
- Complex
- Venue
- Rank Range
- Competitor

All filters dynamically update tables, KPIs, and charts in real-time.

---

## 🛠️ Technology Stack

| Layer              | Technology        |
|--------------------|-------------------|
| Programming        | Python 3.10       |
| Frontend           | Streamlit         |
| Visualization      | Plotly            |
| Data Handling      | Pandas            |
| Database           | SQL Server        |
| API Integration    | SportRadar API    |
| Environment Config | python-dotenv     |
| Version Control    | Git               |
---

## 📂 Project Structure
```
game-analytics-tennis/
│
├── api/
│ ├── competitions_api.py
│ ├── complexes_api.py
│ └── rankings_api.py
│
├── data/raw/
│ ├── competitions.json
│ ├── complexes.json
│ └── double_rankings.json
│
├── database/
│ ├── db_connection.py
│ ├── schema.py
│
├── queries/
│ ├── competition_queries.py
│ ├── ranking_queries.py
│ └── venue_queries.py
│
├── scripts/
│ └── insert_data.py
│
├── app.py
├──tennis_db.sqlite
├── requirements.txt
└── .env
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/Nihaa-20/Tennis-Game-Analysis
cd game-analytics-tennis
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file:
```
DB_SERVER=your_server
DB_DATABASE=tennis_db
DB_USERNAME=your_username
DB_PASSWORD=your_password
```

### 5. Initialize Database
```bash
python database/schema.py
```

### 6. Insert Data
```bash
python scripts/insert_data.py
```

### 7. Run Application
```bash
streamlit run app.py
```

---

## 📈 Analytical Capabilities
- Aggregation queries (COUNT, SUM, AVG)
- Grouping by category, type, gender
- Ranking comparison analysis
- Movement trend categorization
- Top-N analysis
- Drill-down competitor filtering

---

## 🧠 Skills Demonstrated
- API data ingestion & JSON handling
- Database schema design
- SQL analytical query writing
- Data cleaning & transformation
- Dashboard UX structuring
- Modular project architecture
- Error handling & data validation

---

## 🔮 Future Enhancements
- Live API auto-refresh scheduling
- Player head-to-head comparison module
- Tournament bracket visualization
- Deployment on Streamlit Cloud / Azure
- Authentication & role-based access

---

## 👩‍💻 Author
**Fathima Niha**  
BCA Graduate | Data Analytics Enthusiast 

---

## ⭐ Acknowledgment
Data sourced from SportRadar API for academic and analytical purposes.
