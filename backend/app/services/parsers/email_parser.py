import email
import re

from bs4 import BeautifulSoup
from email import policy
from email.parser import BytesParser


URL_REGEX = r"https?://[^\s]+"


def extract_urls(text):
    return re.findall(URL_REGEX, text)


def parse_eml(file_data):

    msg = BytesParser(
        policy=policy.default
    ).parsebytes(file_data)

    sender = msg.get("From")
    subject = msg.get("Subject")

    return_path = msg.get("Return-Path")
    reply_to = msg.get("Reply-To")

    body = ""
    html_body = ""   
    attachments = []

    # Extract email body
    if msg.is_multipart():

        for part in msg.walk():

            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition"))

            # Attachments
            if "attachment" in disposition:

                filename = part.get_filename()
                attachments.append(filename)

            # Plain text body
            elif content_type == "text/plain":

                body += part.get_content()

            # HTML body
            elif content_type == "text/html":

                html = part.get_content()

                html_body += html  

                soup = BeautifulSoup(html, "html.parser")
                body += soup.get_text()

    else:
        body = msg.get_content()

    urls = extract_urls(body)

    return {
        "sender": sender,
        "subject": subject,
        "body": body,
        "html_body": html_body,
        "urls": urls,
        "attachments": attachments,
        "return_path": return_path,
        "reply_to": reply_to
    }