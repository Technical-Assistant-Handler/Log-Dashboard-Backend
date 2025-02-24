import os
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from fastapi import FastAPI
import config


# Email credentials
SENDER_EMAIL = config.SENDER_EMAIL
EMAIL_PASSWORD = config.EMAIL_PASSWORD

# Initialize FastAPI app
app = FastAPI()


def generate_otp_code():
    """Generate a 6-digit OTP code."""
    system_random = random.SystemRandom()
    return system_random.randint(100000, 999999)

def mail_design(verification_code):
    """Generate the HTML content for the email."""
    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Courier New', Courier, monospace;
                background-color: #ffffff;
                margin: 0;
                padding: 0;
                color: #333333;
            }}
            .email-container {{
                max-width: 600px;
                margin: 20px auto;
                background-color: #f9f9f9;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background-color: #000080;
                color: #ffffff;
                padding: 20px;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
            }}
            .content {{
                padding: 30px;
                color: #333333;
            }}
            .content h2 {{
                font-size: 20px;
                margin-bottom: 20px;
                color: #000080;
            }}
            .code-container {{
                text-align: center;
                margin: 30px 0;
            }}
            .code {{
                display: inline-block;
                font-size: 32px;
                font-weight: bold;
                color: #000080;
                background-color: #ffffff;
                padding: 15px 25px;
                border-radius: 5px;
                border: 2px solid #000080;
                font-family: 'Courier New', Courier, monospace;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                background-color: #f1f1f1;
                color: #666666;
                font-size: 14px;
            }}
            .footer a {{
                color: #000080;
                text-decoration: none;
            }}
            .note {{
                font-size: 14px;
                color: #777777;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                Verification Code
            </div>
            <div class="content">
                <h2>Hello,</h2>
                <p>Your verification code is ready. Please use the following code to complete your authentication process:</p>
                <div class="code-container">
                    <div class="code">{verification_code}</div>
                </div>
                <p>This code is valid for a limited time. Do not share it with anyone.</p>
                <div class="note">
                    <p>If you did not request this code, please ignore this email or contact our support team immediately.</p>
                </div>
            </div>
            <div class="footer">
                <p>Best regards,<br><strong>Technical Assistant Team</strong></p>
                <p>Need help? <a href="mailto:{SENDER_EMAIL}">Contact us</a></p>
            </div>
        </div>
    </body>
    </html>
    """

def send_email(receiver_email, subject, body):
    """Send an email using the Gmail SMTP server."""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
        
        
