import os
import requests
from dotenv import load_dotenv
import jinja2


load_dotenv()

domain = os.getenv("MAILGUN_DOMAIN")
template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)


def render_template(template_filename, **context):
    return template_env.get_template(template_filename).render(**context)

def send_simple_message(to, subject, body, html):
    response = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={
            "from": f"Falilou Niang <mailgun@{domain}>",
            "to": [to],
            "subject": subject,
            "text": body,
            "html": html,
        }
    )

    if response.status_code != 200:
        raise Exception(f"Mailgun API error: {response.status_code} - {response.text}")

    return response


def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        "Successfully signed up",
        f"Hi {username}! You have successfully signed up to the Stores REST API.",
        render_template("email/registration.html", username=username)
    )
