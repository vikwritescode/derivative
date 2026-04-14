import sqlite3
import json

def get_debate(uid: str, debate_id: int, db: sqlite3.Connection): 
    """
    Get a single debate from the debates table
    
    :param uid: The UID of the user
    :type uid: str
    :param debate_id: The ID of the debate to retrieve
    :type debate_id: int
    :param db: The Database Connection
    :type db: sqlite3.Connection
    """
    try:
        cur = db.cursor()
        cur.execute("SELECT id, date, position, points, speaks, infoslide, motion, tournament_id FROM debates WHERE id = ? AND user_id = ?", (debate_id, uid))
        row = cur.fetchone()
        if row is None:
            raise RuntimeError("Debate not found")
        cur.execute("""
                SELECT d.id, d.user_id, t.date, d.position, d.points,
                d.speaks, d.infoslide, d.motion, json_group_array(c.category) AS categories, 
                t.name AS tournament_name, d.date as legacy_date, d.tournament_id,
                t.partner AS partner, t.format AS format, d.has_reply, d.reply, d.sp_order
                
                FROM debates d
                LEFT JOIN categories c ON d.id = c.debate_id
                LEFT JOIN tournaments t on t.tournament_id = d.tournament_id
                WHERE d.user_id = ? AND d.id = ?
                GROUP BY d.id
                ORDER BY d.date DESC, d.id;
                    """, (uid, debate_id))
        i = cur.fetchone()
        return {
            "id": i[0],
            "uid": i[1],
            "date": i[2],
            "position": i[3],
            "points": i[4],
            "speaks": i[5],
            "infoslide": i[6],
            "motion": i[7],
            "categories": json.loads(i[8]),
            "tournament": i[9],
            "legacy_date": i[10],
            "tournament_id": i[11],
            "partner": i[12],
            "format": i[13],
            "has_reply": bool(i[14]),
            "reply": i[15],
            "order": i[16]
        }

    except sqlite3.DatabaseError as e:
        raise RuntimeError("Database Error")