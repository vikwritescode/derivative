from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
import os
import json
from functools import lru_cache
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv

class EmailException(Exception):
    pass

security = HTTPBearer()

@lru_cache()
def get_email_whitelist() -> set:
    """Reads the whitelist file. The @lru_cache ensures this only runs once."""
    # Assuming the app is run from the project root. 
    # Adjust path if necessary (e.g., os.path.join(os.path.dirname(__file__), "..."))
    with open("../whitelist.json", "r") as f:
        return set(json.load(f))


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    email_whitelist: set = Depends(get_email_whitelist)) -> dict:
    try:
        id_token = credentials.credentials
        decoded_token = auth.verify_id_token(id_token)
        
        if (decoded_token["email"] not in email_whitelist) and (not decoded_token["email_verified"]):
            raise EmailException
    
        return decoded_token
    
    except EmailException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not authorized",
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Failed to Authenticate: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def init_firebase():
    load_dotenv()
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.getenv("SERVICE_ACCT_KEY"))
        firebase_admin.initialize_app(cred)