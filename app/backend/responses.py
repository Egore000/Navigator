from fastapi import status
from fastapi.responses import JSONResponse

SuccessResponse = JSONResponse(
    content={"detail": "success"},
    status_code=status.HTTP_200_OK
)

CreatedSuccessfullyResponse = JSONResponse(
    content={"detail": "created successfully"},
    status_code=status.HTTP_201_CREATED
)

DeletedSuccessfullyResponse = JSONResponse(
    content={"detail": "deleted successfully"},
    status_code=status.HTTP_200_OK
)
