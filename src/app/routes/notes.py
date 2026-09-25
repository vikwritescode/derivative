from fastapi import APIRouter, Depends, HTTPException, status, Request
import sqlite3
from app.dependencies import get_current_user
from app.database import get_db
import service
from models import NotFoundError, CategoryList

router = APIRouter(prefix="/api/notes", tags=["notes"])

@router.get("/{debate_id}")
def get_notes_for_debate(debate_id: int, request: Request, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Get notes for a debate.
    
    :param debate_id: id of the debate
    :type debate_id: int
    :param user: firebase user
    :type user: dict
    :param db: sqlite3 database connection
    :type db: sqlite3.Connection
    """
    try:
        return service.get_notes_for_debate(debate_id, user["uid"], db)
    except NotFoundError as e:
        print("Whoopsie")
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/add/{debate_id}")
def write_notes_for_debate(debate_id: int, 
                           note: str,
                           request: Request,
                           user: dict = Depends(get_current_user), 
                           db: sqlite3.Connection = Depends(get_db)):
    try:
        return service.write_notes_for_debate(debate_id, note, user["uid"], db)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        