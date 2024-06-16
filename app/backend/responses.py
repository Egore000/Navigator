from fastapi.responses import JSONResponse
from fastapi import status


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
