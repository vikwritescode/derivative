import sqlite3
from models import TournamentCreate
from utils import correct_name
def create_user_tournament(tournament: TournamentCreate, uid: str, db: sqlite3.Connection):
    """
    Insert a single tournament record into the SQL table
    
    :param tournament: The details of the record
    :type debate: TournamentCreate
    :param uid: The UID of the user
    :type uid: str
    :param db: The Database Connection
    :type db: sqlite3.Connection
    """
    try:
        cur = db.cursor()
        cur.execute("INSERT INTO tournaments (user_id, date, name, speaker_standing, team_standing, rooms, partner, format) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (uid, tournament.date, tournament.name, tournament.speaker_rank, tournament.team_rank, tournament.rooms, correct_name(tournament.partner), tournament.t_format))
        db.commit()
        return cur.lastrowid
    except sqlite3.DatabaseError as e:
        raise RuntimeError("Database Error")