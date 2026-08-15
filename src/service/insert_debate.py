import sqlite3
from models import DebateCreate
from ai import classify
from fastapi import Request

def insert_debate(debate: DebateCreate, uid: str, db: sqlite3.Connection, request: Request):
    """
    Insert a single debate result into the SQL table
    
    :param debate: The details of the record
    :type debate: DebateCreate
    :param uid: The UID of the user
    :type uid: str
    :param db: The Database Connection
    :type db: sqlite3.Connection
    """
    try:
        cur = db.cursor()
        # check if tournament exists before inserting
        if debate.tournament is None:
            # insert without tournament reference if None
            cur.execute("INSERT INTO debates (user_id, date, position, points, speaks, infoslide, motion, sp_order, has_reply, reply) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (uid, debate.date, debate.position, debate.points, debate.speaks, debate.infoslide, debate.motion, debate.order, debate.has_reply, debate.reply))
        else:
            # check if tournament exists
            cur.execute("SELECT tournament_id from tournaments WHERE user_id = ? AND tournament_id = ?",
                        (uid, debate.tournament))
            if cur.fetchone() is None:
                raise RuntimeError("Invalid Tournament ID")
            
            # add tournament to 
            cur.execute("INSERT INTO debates (user_id, date, position, points, speaks, infoslide, motion, tournament_id, sp_order, has_reply, reply) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (uid, debate.date, debate.position, debate.points, debate.speaks, debate.infoslide, debate.motion, debate.tournament, debate.order, debate.has_reply, debate.reply))
            debate_id = cur.lastrowid
            # run classifier to get categories and combine with manual categories
            cats = classify(debate.infoslide, debate.motion, request)
            all_cats = list(set(cats + debate.categories)) if debate.categories is not None else cats
            # insert categories into categories table
            tuples = [(debate_id, uid, c) for c in all_cats]
            cur.executemany("INSERT INTO categories (debate_id, user_id, category) VALUES (?, ?, ?)", tuples)
            
        db.commit()
        return cur.lastrowid
    except sqlite3.DatabaseError as e:
        raise RuntimeError("Database Error")
    
    