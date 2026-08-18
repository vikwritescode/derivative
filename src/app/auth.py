from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
import os
import json
from functools import lru_cache
from pathlib import Path
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv

DEFAULT_SERVICE_ACCT_KEY = "/run/secrets/serviceAccountKey.json"

class EmailException(Exception):
    pass

security = HTTPBearer()

@lru_cache()
def get_whitelist() -> set:
    with open("../whitelist.json", "r") as f:
        return set(json.load(f))


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    whitelist: set = Depends(get_whitelist)) -> dict:
    try:
        id_token = credentials.credentials
        decoded_token = auth.verify_id_token(id_token)
        
        if (decoded_token["uid"] not in whitelist) and (not decoded_token["email_verified"]):
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
        service_acct_key = Path(os.getenv("SERVICE_ACCT_KEY", DEFAULT_SERVICE_ACCT_KEY)).expanduser().resolve()
        if service_acct_key.is_dir():
            service_acct_key = service_acct_key / "serviceAccountKey.json"

        if not service_acct_key.exists() or not service_acct_key.is_file():
            raise FileNotFoundError(
                f"Firebase service account key not found at {service_acct_key}. "
                "Mount the secret file there, or mount a directory containing serviceAccountKey.json."
            )
        cred = credentials.Certificate(str(service_acct_key))
        firebase_admin.initialize_app(cred)