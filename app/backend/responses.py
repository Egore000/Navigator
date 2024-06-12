from fastapi.responses import JSONResponse
from fastapi import status


SuccessResponse = JSONResponse(
    content="success",
    status_code=status.HTTP_200_OK
)

CreatedSuccessfullyResponse = JSONResponse(
    content="created successfully",
    status_code=status.HTTP_201_CREATED
)

DeletedSuccessfullyResponse = JSONResponse(
    content="deleted successfully",
    status_code=status.HTTP_200_OK
)
