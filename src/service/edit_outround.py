import sqlite3
from models import OutroundCreate

def edit_outround(outround_id, outround: OutroundCreate, uid: str, db: sqlite3.Connection):
    """
    Edit a single outround in the outrounds table
    
    :param outround: The details of the record
    :type outround: OutroundCreate
    :param uid: The UID of the user
    :type uid: str
    :param db: The Database Connection
    :type db: sqlite3.Connection
    """
    try:
        cur = db.cursor()
        # delete old categories for the outround
        cur.execute("DELETE FROM outround_categories WHERE outround_id = ? AND user_id = ?", (outround_id, uid))
        
        # check if outround exists before updating
        cur.execute("SELECT id FROM outrounds WHERE id = ? AND user_id = ?", (outround_id, uid))
        if cur.fetchone() is None:
            raise RuntimeError("Outround not found")
        
        # check if tournament exists before updating
        if outround.tournament is None:
            # update without tournament reference
            cur.execute("UPDATE outrounds SET position = ?, advancing = ?, round_name = ?, round_short_name = ?, infoslide = ?, motion = ?, sp_order = ?, has_reply = ?, tournament_id = NULL WHERE id = ? AND user_id = ?",
                        (outround.position, outround.advancing, outround.round_name, outround.round_short_name, outround.infoslide, outround.motion, outround.order, outround.has_reply, outround_id, uid))
        else:
            # check if tournament exists
            cur.execute("SELECT tournament_id from tournaments WHERE user_id = ? AND tournament_id = ?",
                        (uid, outround.tournament))
            if cur.fetchone() is None:
                raise RuntimeError("Invalid Tournament ID")
            
            # update outround with tournament
            cur.execute("UPDATE outrounds SET position = ?, advancing = ?, round_name = ?, round_short_name = ?, infoslide = ?, motion = ?, sp_order = ?, has_reply = ?, tournament_id = ? WHERE id = ? AND user_id = ?",
                        (outround.position, outround.advancing, outround.round_name, outround.round_short_name, outround.infoslide, outround.motion, outround.order, outround.has_reply, outround.tournament, outround_id, uid))
            
        # insert categories for the outround (if supported by OutroundCreate object)
        if hasattr(outround, 'categories') and outround.categories:
            cur.executemany("INSERT INTO outround_categories (outround_id, user_id, category) VALUES (?, ?, ?)",
                        [(outround_id, uid, category.value) for category in outround.categories.categories])
                
            
        db.commit()
        return outround_id
    except sqlite3.DatabaseError as e:
        raise RuntimeError("Database Error")
    
    