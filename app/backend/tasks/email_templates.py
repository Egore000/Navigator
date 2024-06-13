from email.message import EmailMessage
from app.config import settings


def create_booking_confirmation_template(
        booking: dict,
        email_to: EmailMessage,
):
    email = EmailMessage()

    email["Subject"] = "Подтверждение"
    email["From"] = settings.smtp.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Подтвердите бронь</h1>
            Вы забронировали отель с {booking["date_from"]} по {booking["date_to"]}
        """,
        subtype="html",
    )
    return email
