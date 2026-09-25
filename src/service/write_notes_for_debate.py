import sqlite3
from models import NotFoundError
def write_notes_for_debate(debate_id: int,
                           note: str,
                           uid: str,
                           db: sqlite3.Connection):
    """
    write/overwrite notes associated with a debate
    
    :param debate_id: debate ID
    :type debate_id: int
    :param note: debate notes
    :typr note: str
    :param uid: user id
    :type uid: str
    :param db: sqlite3 database
    :type db: sqlite3.Database
    :return: notes associated with a debate if they exist
    :rtype: string
    """
    cur = db.cursor()
    
    # check if the debate exists
    cur.execute(
        """
        SELECT id FROM debates 
        WHERE id=?
        AND user_id=?
        """, (debate_id, uid))
    record = cur.fetchone()
    if record is None:
        raise NotFoundError
    # overwrite the notes
    cur.execute("""
        INSERT OR REPLACE INTO NOTES (user_id, debate_id, note)
        VALUES (?, ?, ?)
    """, (uid, debate_id, note))
    db.commit()
    