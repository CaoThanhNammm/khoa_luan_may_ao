import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

load_dotenv()

# Email configuration
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_TLS = os.getenv("MAIL_TLS", "True").lower() == "true"
MAIL_SSL = os.getenv("MAIL_SSL", "False").lower() == "true"

# Set up Jinja2 template environment
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
env = Environment(loader=FileSystemLoader(template_dir))

def send_email(to_email: str, subject: str, template_name: str, context: dict):
    """
    Send an email using a template
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        template_name: Name of the template file (without extension)
        context: Dictionary of variables to pass to the template
    """
    # Create message
    message = MIMEMultipart()
    message["From"] = MAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject
    
    # Render template
    template = env.get_template(f"{template_name}.html")
    html_content = template.render(**context)
    
    # Attach HTML content
    message.attach(MIMEText(html_content, "html"))
    
    # Connect to server and send email
    try:
        if MAIL_SSL:
            server = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
        else:
            server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
            if MAIL_TLS:
                server.starttls()
        
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(MAIL_FROM, to_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

def send_password_reset_email(to_email: str, reset_token: str):
    """Send a password reset email"""
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    reset_url = f"{frontend_url}/reset-password?token={reset_token}"
    
    context = {
        "reset_url": reset_url,
        "support_email": MAIL_FROM
    }
    
    return send_email(
        to_email=to_email,
        subject="Đặt lại mật khẩu",
        template_name="password_reset",
        context=context
    )