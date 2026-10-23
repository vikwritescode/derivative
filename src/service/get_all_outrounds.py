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
                SELECT o.id, o.user_id, o.position, o.advancing, o.round_name, o.round_short_name,
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
             "position": i[2],
             "advancing": i[3],
             "round_name": i[4],
             "round_short_name": i[5],
             "infoslide": i[6],
             "motion": i[7],
             "categories": [c for c in json.loads(i[8]) if c is not None],
             "tournament": i[9],
             "tournament_id": i[10],
             "partner": i[11],
             "format": i[12],
             "has_reply": bool(i[13]),
             "order": i[14]
        } for i in x]
        return r
    except sqlite3.Error as e:
        print(e)
        raise RuntimeError("Database Issue")
    
    