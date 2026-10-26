from fastapi import APIRouter, Depends, HTTPException, status, Request
import sqlite3
from app.dependencies import get_current_user
from app.database import get_db
import service
from models import OutroundCreate, NotFoundError

router = APIRouter(prefix="/api/outrounds", tags=["outrounds"])

@router.get("/get")
def api_get(user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Fetch all outrounds for a user    
    :param user: user dictionary (firebase)
    :type user: dict
    :param db: sqlite database connection
    :type db: sqlite3.Connection
    """
    try:
        f = service.get_all_outrounds(user["uid"], db)
        return {"outrounds": f}
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))

@router.post("/add")
def api_post(outround: OutroundCreate, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db), request: Request = None):
    """
    Add another outround to the database.
    
    :param outround: Data for the table
    :type outround: OutroundCreate
    :param user: the user object
    :type user: dict
    :param db: sqlite3 database connection
    :type db: sqlite3.Connection
    """
    try:
        attempt = service.insert_outround(outround, user["uid"], db, request)
        return {"id": attempt, "message": "Successfully inserted record"}
    except RuntimeError as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

@router.get("/get/{outround_id}")
def api_get_debate(outround_id: int, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Get debate index {outround_id} if it exists and is owned by user
    
    :param outround_id: The debate to get
    :type outround_id: int
    :param user: firebase user
    :type user: dict
    :param db: sqlite3 database object
    :type db: sqlite3.Connection, request: Request = None
    """
    try:
        return service.get_outround(user["uid"], outround_id, db)
    except RuntimeError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User Record Not Found")

@router.post("/edit")
def api_post(outround_id: int, outround: OutroundCreate, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Edit details of outround in outrounds table.
    
    :param debate_id: id of the debate to edit
    :type debate_id: int
    :param debate: Data for the table
    :type debate: DebateCreate
    :param user: the user object
    :type user: dict
    :param db: sqlite3 database connection
    :type db: sqlite3.Connection
    """
    try:
        attempt = service.edit_outround(outround_id, outround, user["uid"], db)
        return {"id": attempt, "message": "Successfully edited record"}
    except RuntimeError as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))  
  
@router.delete("/delete/{outround_id}")
def api_delete_outround(outround_id: int, user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    """
    Delete outround index {outround_id} if it exists and is owned by user
    
    :param outround_id: The outround to delete
    :type outround_id: int
    :param user: firebase user
    :type user: dict
    :param db: sqlite3 database object
    :type db: sqlite3.Connection, request: Request = None
    """
    try:
        return service.delete_outround(user["uid"], outround_id, db)
    except RuntimeError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User Record Not Found")