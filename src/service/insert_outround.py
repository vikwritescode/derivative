import sqlite3
from models import OutroundCreate
from ai import classify
from fastapi import Request

def insert_outround(outround: OutroundCreate, uid: str, db: sqlite3.Connection, request: Request):
    """
    Insert a single outround result into the SQL table
    
    :param outround: The details of the record
    :type outround: OutroundCreate
    :param uid: The UID of the user
    :type uid: str
    :param db: The Database Connection
    :type db: sqlite3.Connection
    """
    try:
        cur = db.cursor()
        # check if tournament exists before inserting
        if outround.tournament is None:
            raise RuntimeError("Tournament ID is required for outrounds")
        else:
            # check if tournament exists
            cur.execute("SELECT tournament_id from tournaments WHERE user_id = ? AND tournament_id = ?",
                        (uid, outround.tournament))
            if cur.fetchone() is None:
                raise RuntimeError("Invalid Tournament ID")
            
            # add tournament to 
            cur.execute("INSERT INTO outrounds (user_id, tournament_id, position, sp_order, round_name, round_short_name, advancing, infoslide, motion, has_reply) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (uid, outround.tournament, outround.position, outround.order, outround.round_name, outround.round_short_name, outround.advancing, outround.infoslide, outround.motion, outround.has_reply))
            outround_id = cur.lastrowid
            # run classifier to get categories and combine with manual categories
            cats = classify(outround.infoslide, outround.motion, request)
            manual_categories = outround.categories.categories if outround.categories else []
            all_cats = list(set(cats + manual_categories))
            # insert categories into categories table
            tuples = [(outround_id, uid, c) for c in all_cats]
            cur.executemany("INSERT INTO outround_categories (outround_id, user_id, category) VALUES (?, ?, ?)", tuples)
            
        db.commit()
        return cur.lastrowid
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError("Database Error")
    
    