import time
import requests
from fastapi import Form, Depends, File
from fastapi import APIRouter, UploadFile, HTTPException
from sqlalchemy.orm import Session

from core.config import settings
from db.session import get_db
from db.repository.csam_ratio import get_db_data
from schemas.ng import ShowNG

from apis.inspect.base import inspect


router = APIRouter()


@router.post("/upload_file", response_model=ShowNG)
def predict_NG_chips(
    file: UploadFile = File(...), lot_no: str = Form(...), db: Session = Depends(get_db)
):
    print("Received file to process, please wait...")
    start = time.time()
    # Check if lot number exists or if its for testing
    if lot_no.lower()[:4] == "test":
        chip_type = settings.CHIPTYPE
    else:
        prass = requests.get(settings.PRASS_URL + lot_no).json()
        if prass[settings.LOT_NO_COL] == None:
            raise HTTPException(
                status_code=404, detail=f"Lot number: {lot_no} not found in database"
            )
        chip_type = prass[settings.CHIP_TYPE_COL]
    try:
        chips_dict, save_dir, img_shape, no_of_batches, no_of_chips = inspect(
            file, lot_no, db
        )
    except:
        raise HTTPException(
            status_code=400, detail=f"Error while processing uploaded file"
        )

    res = ShowNG(
        plate_no=file.filename.split(".")[0],
        chips=chips_dict,
        img_shape=img_shape,
        no_of_chips=no_of_chips,
        no_of_batches=no_of_batches,
        directory=save_dir,
        chip_type=chip_type,
    )

    print(f"Total Time taken: {round(time.time()-start,2)}")

    return res


@router.get("/read_db")
def read_db(db: Session = Depends(get_db)):
    ratio = get_db_data(db=db)
    return ratio
