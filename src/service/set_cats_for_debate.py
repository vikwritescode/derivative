from models import NotFoundError, CategoryList
import sqlite3

def set_cats_for_debate(debate_id: int, categories: CategoryList, uid: str, db: sqlite3.Connection):
    """
    Edit debate categories.
    
    :param debate_id: id of the debate
    :type debate_id: int
    :param categories: list of categories to set for the debate
    :type categories: list[str]
    :param uid: firebase user id
    :type uid: str
    :param db: sqlite3 database connection
    :type db: sqlite3.Connection
    """
    try:
        cursor = db.cursor()
        # check if debate exists and user has access to it
        cursor.execute("SELECT id FROM debates WHERE id = ? AND user_id = ?", (debate_id, uid))
        if not cursor.fetchone():
            raise NotFoundError("Debate not found")
        
        # get unique categories from the input
        unique_categories = list(set(categories))
        
        # delete old categories
        cursor.execute("DELETE FROM categories WHERE debate_id = ? AND user_id = ?", (debate_id, uid))

        # insert new categories
        cursor.executemany("INSERT INTO categories (debate_id, user_id, category) VALUES (?, ?, ?)",
                           [(debate_id, uid, category.value) for category in unique_categories])
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise e