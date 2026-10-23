import sqlite3
from models import NotFoundError

def delete_outround(uid: str, outround_id: int, db: sqlite3.Connection) -> dict:
    """
    Delete record if owned by UID
    
    :param uid: Description
    :type uid: str
    :param outround_id: Outround ID (primary key)
    :type outround_id: int
    :param db: sqlite3 database connection
    :type db: sqlite3.Connection
    :return: Success Message
    :rtype: dict
    """
    try:
        cur = db.cursor()
        cur.execute("SELECT 1 from outrounds WHERE user_id=? AND id=?", (uid, outround_id))
        recs = cur.fetchall()
        if len(recs) == 0:
            raise NotFoundError("Record Not Found")
        cur.execute("DELETE FROM outrounds WHERE user_id=? and id=?", (uid, outround_id))
        cur.execute("DELETE FROM outround_categories where outround_id=?", (outround_id, ))
        db.commit()
        return {"message": "record deleted successfully"}
    except NotFoundError as e:
        raise
    except Exception as e:
        raise RuntimeError("Server Error")