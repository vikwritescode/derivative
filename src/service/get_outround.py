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
                SELECT o.id, o.user_id, t.date, o.position, o.advancing, o.round_name,
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
        cts = json.loads(i[9]) if i[9] else []
        return {
            "id": i[0],
            "uid": i[1],
            "date": i[2],
            "position": i[3],
            "advancing": bool(i[4]),
            "round_name": i[5],
            "round_short_name": i[6],
            "infoslide": i[7],
            "motion": i[8],
            "categories": [c for c in cts if c is not None],
            "tournament": i[10],
            "tournament_id": i[11],
            "partner": i[12],
            "format": i[13],
            "has_reply": bool(i[14]),
            "order": i[15]
        }

    except NotFoundError:
        raise
    except sqlite3.DatabaseError as e:
        raise RuntimeError("Database Error")