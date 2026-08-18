import os
import sqlite3

DEFAULT_DB_PATH = os.getenv("DB_PATH", "debates.db")


def create_tables(db_path: str = DEFAULT_DB_PATH):
    db_directory = os.path.dirname(db_path)
    if db_directory:
        os.makedirs(db_directory, exist_ok=True)

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # create us a table for BP debates if not already there
    cur.execute("""
    CREATE TABLE IF NOT EXISTS debates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        date DATE NOT NULL,
        position TEXT NOT NULL CHECK(position IN ('OG', 'OO', 'CG', 'CO', 'AFF', 'NEG', 'ABS')),
        sp_order INTEGER NOT NULL CHECK("sp_order" >= 0 AND "sp_order" <= 3) DEFAULT 0,
        points INTEGER NOT NULL CHECK(points >= 0 AND points <= 3),
        speaks INTEGER NOT NULL,
        infoslide TEXT NOT NULL,
        motion TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        reply INTEGER NOT NULL DEFAULT 0,
        has_reply BIT NOT NULL DEFAULT 0);
                """)
    
    # attempt to add this column, should allow migration from older values
    try:
        cur.execute("ALTER TABLE debates ADD COLUMN tournament_id INTEGER REFERENCES Tournaments(tournament_id);")
    except sqlite3.OperationalError as e:
        if "duplicate column name: tournament_id" not in str(e):
            raise
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        debate_id INTEGER NOT NULL,
        user_id TEXT NOT NULL,
        category TEXT NOT NULL CHECK(category IN (
            'Africa',
            'Animal Rights',
            'Art',
            'Artificial Intelligence',
            'Asia',
            'Australia',
            'Charity',
            'Children',
            'Cities',
            'Climate Change',
            'Colonialism',
            'Criminal Justice',
            'Culture',
            'Cybersecurity',
            'Democracy',
            'Development',
            'Disability Rights',
            'Drugs',
            'Economics',
            'Education/Academia',
            'Elderly/Aging',
            'Energy',
            'Environment',
            'Ethics',
            'Europe',
            'Feminism',
            'Healthcare',
            'Historical Memory',
            'Housing',
            'Human Rights',
            'Immigration',
            'Indigenous People',
            'International Relations',
            'Labor',
            'Latin America',
            'Law',
            'LGBTQ+',
            'Media',
            'Medical',
            'Mental Health',
            'Middle East',
            'Military',
            'Minority Communities',
            'Nationalism',
            'Philosophy',
            'Police',
            'Policy',
            'Politics',
            'Privacy',
            'Private Property',
            'Refugees/Asylum',
            'Religion',
            'Romance/Sex',
            'Romance/Sexuality',
            'Science/Technology',
            'Social Justice',
            'Social Policy',
            'Sports',
            'Terrorism',
            'Trade'
        )),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tournaments (
        tournament_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        user_id TEXT NOT NULL,
        date DATE NOT NULL,
        speaker_standing INTEGER NOT NULL default 0,
        team_standing INTEGER NOT NULL default 0,
        rooms INTEGER NOT NULL default 0,
        format TEXT NOT NULL CHECK(format IN ('BP', 'WSDC', 'AUS')) DEFAULT 'BP',
        partner TEXT,
        tab_url TEXT,
        speaker_url TEXT,
        slug TEXT
    );
    """)
    
    con.commit()
    con.close()

def get_db(db_path: str = DEFAULT_DB_PATH):
    """
    function to pass database connections to the service layer,
    closing even if errors occur
    """
    # FastAPI may execute sync dependencies/endpoints on worker threads,
    # so disable sqlite's same-thread guard for request-scoped connections.
    conn = sqlite3.connect(db_path, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close() 

