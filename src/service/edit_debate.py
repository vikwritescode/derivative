import sqlite3
from models import DebateCreate
def edit_debate(debate_id, debate: DebateCreate, uid: str, db: sqlite3.Connection):
    """
    Edit a single debate in the debates table
    
    :param debate: The details of the record
    :type debate: DebateCreate
    :param uid: The UID of the user
    :type uid: str
    :param db: The Database Connection
    :type db: sqlite3.Connection
    """
    try:
        cur = db.cursor()
        # delete old categories for the debate
        cur.execute("DELETE FROM categories WHERE debate_id = ? AND user_id = ?", (debate_id, uid))
        
        # check if debate exists before updating
        cur.execute("SELECT id FROM debates WHERE id = ? AND user_id = ?", (debate_id, uid))
        if cur.fetchone() is None:
            raise RuntimeError("Debate not found")
        
        # check if tournament exists before updating
        if debate.tournament is None:
            # update without tournament reference
            cur.execute("UPDATE debates SET date = ?, position = ?, points = ?, speaks = ?, infoslide = ?, motion = ?, tournament_id = NULL WHERE id = ? AND user_id = ?",
                        (debate.date, debate.position, debate.points, debate.speaks, debate.infoslide, debate.motion, debate_id, uid))
        else:
            # check if tournament exists
            cur.execute("SELECT tournament_id from tournaments WHERE user_id = ? AND tournament_id = ?",
                        (uid, debate.tournament))
            if cur.fetchone() is None:
                raise RuntimeError("Invalid Tournament ID")
            
            # update debate with tournament
            cur.execute("UPDATE debates SET date = ?, position = ?, points = ?, speaks = ?, infoslide = ?, motion = ?, tournament_id = ? WHERE id = ? AND user_id = ?",
                        (debate.date, debate.position, debate.points, debate.speaks, debate.infoslide, debate.motion, debate.tournament, debate_id, uid))
            
        # insert categories for the debate (if supported by DebateCreate object)
        if hasattr(debate, 'categories') and debate.categories:
            cur.execute("DELETE FROM categories WHERE debate_id = ? AND user_id = ?", (debate_id, uid))
            cur.executemany("INSERT INTO categories (debate_id, user_id, category) VALUES (?, ?, ?)",
                        [(debate_id, uid, category.value) for category in debate.categories.categories])
                
            
        db.commit()
        return debate_id
    except sqlite3.DatabaseError as e:
        raise RuntimeError("Database Error")
    
    