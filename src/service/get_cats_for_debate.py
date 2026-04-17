import sqlite3
def get_cats_for_debate(debate_id: int, uid: str, db: sqlite3.Connection):
    """
    Get categories for a debate.
    :param debate_id: id of the debate
    :type debate_id: int
    :param uid: user id
    :type user: str
    :param db: sqlite3 database connection
    :type db: sqlite3.Connection
    """
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id FROM debates WHERE id = ?", (debate_id,))
        cursor = db.cursor()
        cursor.execute("SELECT category FROM categories WHERE debate_id = ? AND user_id = ?", (debate_id, uid))
        result = cursor.fetchall()
        if not result:
            return []
        return [row[0] for row in result]
    except Exception as e:
        raise e

    