from decouple import config as getenv
from email.message import EmailMessage
import smtplib


def send_email(subject, content):
    port = 465
    smtp_server = getenv("SMTP_SERVER")
    sender_email = getenv("SENDER_EMAIL")
    receiver_email = getenv("RECEIVER_EMAIL")
    password = getenv("SENDER_PW")

    server = smtplib.SMTP_SSL(smtp_server, port)
    server.ehlo()
    server.login(sender_email, password)

    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = 'Price Alert Bot' + f' <{sender_email}>'
    msg['To'] = receiver_email

    server.send_message(msg)
    print("Server sent mail")

