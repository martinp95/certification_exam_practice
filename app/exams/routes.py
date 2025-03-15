from typing import List
from fastapi import APIRouter, Depends, HTTPException

from exams.logic import find_all_certifications
from auth.security import get_current_user
from exams.schemas import CertificationSchema

router = APIRouter()


@router.get("/certifications", tags=["Certifications"], response_model=List[CertificationSchema])
def get_certifications(current_user=Depends(get_current_user)):
    """
    Retrieve certifications after verifying the provided JWT token.

    Returns:
        List[CertificationSchema]: A list of certification objects.
    """
    if not current_user or "username" not in current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    certifications = find_all_certifications()

    return certifications
