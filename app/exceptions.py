from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"    


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истёк"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Ошибка авторизации"


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserDoesNotExistsException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class AccessForbiddenException(BookingException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Доступ запрещён" 


class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"


class NotFoundError(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Объект не найден"