import os
import json
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "CSAM Defects Collect (CDC)"
    PROJECT_VERSION: str = "1.0.0"

    DBTYPE: str = os.getenv("DBTYPE")
    USER: str = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    SERVER: str = os.getenv("SERVER", "localhost")
    PORT: str = os.getenv("PORT", 5432)  # default postgres port is 5432
    DB: str = os.getenv("DB", "tdd")
    DATABASE_URL = f"{DBTYPE}://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB}"

    ORIGIN: list = json.loads(os.getenv("ORIGIN"))
    PRASS_URL: str = os.getenv("PRASS_URL")
    LOT_NO_COL: str = os.getenv("LOT_NO_COL")
    CHIP_TYPE_COL: str = os.getenv("CHIP_TYPE_COL")
    CHIPTYPE: str = os.getenv("CHIPTYPE")

    REALTIMEDB: str = os.getenv("REALTIMEDB")
    TABLEID: str = os.getenv("TABLEID")

    IMAGESIZE: list = [54, 54]


settings = Settings()
