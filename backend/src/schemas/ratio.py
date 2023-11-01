from pydantic import BaseModel


class CreateBaseData(BaseModel):
    lot_no: str
    plate_no: str
    ng_list: list
    others_list: list
    no_of_batches: int
    no_of_chips: int
    no_of_ng: int
    no_of_others: int
    directory: str
    chip_type: str
