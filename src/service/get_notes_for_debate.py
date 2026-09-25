from fastapi import Request
import sqlite3
def get_notes_for_debate(debate_id: str, uid: str, db: sqlite3.Connection):
    """
    Get Notes associated with a debate
    
    :param debate_id: debate ID
    :type debate_id: int
    :param uid: tournament slug
    :type uid: str
    :param db: sqlite3 database
    :type db: sqlite3.Database
    :return: notes associated with a debate if they exist
    :rtype: string
    """
    try:
        cur = db.cursor()
        cur.execute("""
                    SELECT note FROM NOTES
                    WHERE user_id=?
                    AND debate_id=?
                    """, (uid, debate_id))
        l = cur.fetchone()
        return l[0] if l else None
        
    except sqlite3.DatabaseError as e:
        raise
    