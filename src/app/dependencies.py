import os
from pathlib import Path
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv

DEFAULT_SERVICE_ACCT_KEY = "/run/secrets/serviceAccountKey.json"

from .auth import get_current_user

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