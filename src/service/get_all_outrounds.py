import sqlite3
import json

def get_all_outrounds(uid: str, db_conn: sqlite3.Connection) -> list:
    """
    Get all debates associated with a user
    
    :param uid: firebase uid
    :type uid: str
    :param db_conn: sqlite3 database connection
    :type db_conn: sqlite3.Connection
    :return: list of debates associated with user
    :rtype: list
    """
    try:
        cur = db_conn.cursor()
        cur.execute("""
                SELECT o.id, o.user_id, t.date, o.position, o.advancing, o.round_name, o.round_short_name,
                o.infoslide, o.motion, json_group_array(c.category) AS categories, 
                t.name AS tournament_name, o.tournament_id,
                t.partner AS partner, t.format AS format, o.has_reply, o.sp_order
                
                FROM outrounds o
                LEFT JOIN outround_categories c ON o.id = c.outround_id
                LEFT JOIN tournaments t on t.tournament_id = o.tournament_id
                WHERE o.user_id = ?
                GROUP BY o.id
                ORDER BY t.date DESC, o.id;
                    """, (uid,))
        x = cur.fetchall()
        r = [
            {"id": i[0],
             "uid": i[1],
             "date": i[2],
             "position": i[3],
             "advancing": bool(i[4]),
             "round_name": i[5],
             "round_short_name": i[6],
             "infoslide": i[7],
             "motion": i[8],
             "categories": [c for c in json.loads(i[9]) if c is not None],
             "tournament": i[10],
             "tournament_id": i[11],
             "partner": i[12],
             "format": i[13],
             "has_reply": bool(i[14]),
             "order": i[15]
        } for i in x]
        return r
    except sqlite3.Error as e:
        print(e)
        raise RuntimeError("Database Issue")
    
    