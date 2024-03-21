from typing import List

from fastapi import APIRouter, Depends, HTTPException

import src.auth as auth
from src.db import DB, get_db
from src.models import Compute, Compute_all, Mode, Results

router = APIRouter(prefix="/calculator")


@router.post("/compute/", response_model=Compute)
def compute(
    number: int,
    mode: Mode = "SUM",
    db: DB = Depends(get_db),
    authorized: bool = Depends(auth.validate),
) -> Compute:
    db_num = db.get_number()

    if mode == "SUM":
        result = Results(addition=(number + db_num))
    elif mode == "SUB":
        result = Results(subtraction=(number - db_num))
    elif mode == "PROD":
        result = Results(multiplication=(number * db_num))
    elif mode == "ALL":
        result = Results(
            addition=(number + db_num),
            subtraction=(number - db_num),
            multiplication=(number * db_num),
        )
    else:
        raise HTTPException(status_code=404, detail="Incorrect mode")

    returns = Compute(db_number=db_num, results=result)
    return returns


@router.post("/compute_all/", response_model=Compute_all)
def compute_all(
    numbers: List[int],
    mode: Mode = "SUM",
    db: DB = Depends(get_db),
    authorized: bool = Depends(auth.validate),
) -> Compute_all:
    db_num = db.get_number()

    results = []
    for num in numbers:
        if mode == "SUM":
            results.append(Results(addition=(num + db_num)))
        elif mode == "SUB":
            results.append(Results(subtraction=(num - db_num)))
        elif mode == "PROD":
            results.append(Results(multiplication=(num * db_num)))
        elif mode == "ALL":
            results.append(
                Results(
                    addition=(num + db_num),
                    subtraction=(num - db_num),
                    multiplication=(num * db_num),
                )
            )
        else:
            raise HTTPException(status_code=404, detail="Incorrect mode")

    returns = Compute_all(db_number=db_num, results=results)
    return returns
