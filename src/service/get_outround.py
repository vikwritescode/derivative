import sqlite3
import json
from models import NotFoundError

def get_outround(uid: str, outround_id: int, db: sqlite3.Connection):
    """
    Get a single outround from the outrounds table.
    
    :param uid: The UID of the user
    :type uid: str
    :param outround_id: The ID of the outround to retrieve
    :type outround_id: int
    :param db: The Database Connection
    :type db: sqlite3.Connection
    """
    try:
        cur = db.cursor()
        cur.execute("""
                SELECT o.id, o.user_id, o.position, o.advancing, o.round_name,
                o.round_short_name, o.infoslide, o.motion,
                json_group_array(c.category) AS categories,
                t.name AS tournament_name, o.tournament_id,
                t.partner AS partner, t.format AS format, o.has_reply, o.sp_order
                
                FROM outrounds o
                LEFT JOIN outround_categories c ON o.id = c.outround_id
                LEFT JOIN tournaments t ON t.tournament_id = o.tournament_id
                WHERE o.user_id = ? AND o.id = ?
                GROUP BY o.id;
                    """, (uid, outround_id))
        i = cur.fetchone()
        if i is None:
            raise NotFoundError("Outround not found")
        cts = json.loads(i[8]) if i[8] else []
        return {
            "id": i[0],
            "uid": i[1],
            "position": i[2],
            "advancing": bool(i[3]),
            "round_name": i[4],
            "round_short_name": i[5],
            "infoslide": i[6],
            "motion": i[7],
            "categories": [c for c in cts if c is not None],
            "tournament": i[9],
            "tournament_id": i[10],
            "partner": i[11],
            "format": i[12],
            "has_reply": bool(i[13]),
            "order": i[14]
        }

    except NotFoundError:
        raise
    except sqlite3.DatabaseError as e:
        raise RuntimeError("Database Error")