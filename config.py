import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # Si Docker pasa DATABASE_URL → la usa
    if os.getenv("DATABASE_URL"):
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    else:
        # Caso local: usa URL local del .env
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_LOCAL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
