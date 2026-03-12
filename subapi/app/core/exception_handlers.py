from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.app import app
from app.core.exceptions import (
    DatabaseConnectionException,
    InvalidIdException,
    UserNotFoundException,
    UserAlreadyExistsException,
    UserUnauthorizedException,
    TokenExpiredSignatureException,
    TokenInvalidSignatureException,
    SubscriptionNotFoundException,
    SubscriptionAlreadyExistsException,
    TopicNotFoundException,
    TopicAlreadyExistsException,
    ItemNotFoundException,
)


@app.exception_handler(DatabaseConnectionException)
async def database_connection_exception_handler(
    request: Request, exc: DatabaseConnectionException
):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Try Again Later"},
    )


@app.exception_handler(InvalidIdException)
async def invalid_id_exception_handler(request: Request, exc: InvalidIdException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Invalid Object Id"},
    )


@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(
    request: Request, exc: UserNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"message": "User Not Found"}
    )


@app.exception_handler(UserAlreadyExistsException)
async def user_already_exists_exception_handler(
    request: Request, exc: UserAlreadyExistsException
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "User with this email already exists"},
    )


@app.exception_handler(UserUnauthorizedException)
async def user_unauthorized_exception_handler(
    request: Request, exc: UserUnauthorizedException
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": "Invalid Credentials"},
    )


@app.exception_handler(TokenExpiredSignatureException)
async def token_expired_signature_exception_handler(
    request: Request, exc: TokenExpiredSignatureException
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Token Expired"}
    )


@app.exception_handler(TokenInvalidSignatureException)
async def token_invalid_signature_exception_handler(
    request: Request, exc: TokenInvalidSignatureException
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Token Invalid"}
    )


@app.exception_handler(SubscriptionNotFoundException)
async def subscription_not_found_exception_handler(
    request: Request, exc: SubscriptionNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "Subscription Not Found"},
    )


@app.exception_handler(SubscriptionAlreadyExistsException)
async def subscription_already_exists_exception_handler(
    request: Request, exc: SubscriptionAlreadyExistsException
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Subscription to this topic already exists"},
    )


@app.exception_handler(TopicNotFoundException)
async def topic_not_found_exception_handler(
    request: Request, exc: TopicNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "Topic Not Found"},
    )


@app.exception_handler(TopicAlreadyExistsException)
async def topic_already_exists_exception_handler(
    request: Request, exc: TopicAlreadyExistsException
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Topic already exists"},
    )


@app.exception_handler(ItemNotFoundException)
async def item_not_found_exception_handler(
    request: Request, exc: ItemNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "Item Not Found"},
    )
