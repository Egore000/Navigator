import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.backend.tasks._celery import celery
from app.backend.tasks.email_templates import create_booking_confirmation_template
from app.config import settings


@celery.task
def process_picture(path: str):
    image_path = Path(path)
    image = Image.open(image_path)

    im_resized_1000_500 = image.resize((1000, 500))
    im_resized_200_100 = image.resize((200, 100))
    im_resized_1000_500.save(
        f"app\\frontend\\static\\images\\resized\\1000_500\\resized_{image_path.name}"
    )
    im_resized_200_100.save(
        f"app\\frontend\\static\\images\\resized\\200_100\\resized_{image_path.name}"
    )


@celery.task
def send_booking_confirmation_email(
        booking: dict,
        email_to: EmailStr,
):
    email_to_mock = settings.smtp.SMTP_USER
    msg_content = create_booking_confirmation_template(booking, email_to_mock)

    with smtplib.SMTP_SSL(settings.smtp.SMTP_HOST,
                          settings.smtp.SMTP_PORT) as server:
        server.login(settings.smtp.SMTP_USER, settings.smtp.SMTP_PASS)
        server.send_message(msg_content)
