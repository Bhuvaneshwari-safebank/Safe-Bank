import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config
from flask import url_for

# ✅ Temporary in-memory OTP store
otp_storage = {}

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_email(to, subject, body, is_html=False):
    """Reusable email sending function"""
    msg = MIMEMultipart()
    msg['From'] = config.SMTP_EMAIL
    msg['To'] = to
    msg['Subject'] = subject

    if is_html:
        msg.attach(MIMEText(body, 'html'))
    else:
        msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
        server.starttls()
        server.login(config.SMTP_EMAIL, config.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent to {to}")
    except Exception as e:
        print(f"❌ Failed to send email to {to}: {e}")

def send_otp(receiver_email):
    """Send OTP to the user's registered email"""
    otp = generate_otp()
    otp_storage[receiver_email] = otp

    body = f"""
    Dear User,

    Your OTP for SafeBank transaction is: {otp}

    Please do not share this OTP with anyone.

    Regards,
    SafeBank Team
    """

    send_email(receiver_email, "SafeBank OTP Verification Code", body)

def verify_otp(receiver_email, entered_otp):
    """Verify entered OTP matches"""
    if receiver_email in otp_storage and otp_storage[receiver_email] == entered_otp:
        del otp_storage[receiver_email]
        return True
    return False

def delete_otp(receiver_email):
    """Clear OTP manually (example: after 3 wrong tries)"""
    if receiver_email in otp_storage:
        del otp_storage[receiver_email]

def send_trust_location_email(email, ip, user_agent):
    """Send alert for new location login with trust link"""
    subject = "🚨 SafeBank Alert: Suspicious Login from New Device/IP"
    body = f"""
    Hello,

    A login was detected from a new browser or IP.

    - Browser: {user_agent}
    - IP Address: {ip}

    If this was **NOT you**, please change your password immediately.

    If it was you, you can trust this location by clicking below:
    ✅ https://your-domain.com/trust_location?email={email}&ip={ip}

    Stay Safe,
    SafeBank Security Team
    """
    send_email(email, subject, body)

def send_new_device_alert(receiver_email, device_info, ip_address):
    """Send alert email if new device or IP address detected"""
    subject = "⚠️ SafeBank Alert: New Device Login Detected"
    body = f"""
    Dear User,

    We detected a login from a new device or IP address:

    - Browser Info: {device_info}
    - IP Address: {ip_address}

    If this was not you, please change your password immediately.

    Stay Safe,
    SafeBank Security Team
    """
    send_email(receiver_email, subject, body)

def send_device_confirmation_email(email, device_id, user_id):
    """Send email with YES/NO confirmation links for new device"""
    yes_url = url_for('confirm_device', user_id=user_id, device_id=device_id, response='yes', _external=True)
    no_url = url_for('confirm_device', user_id=user_id, device_id=device_id, response='no', _external=True)

    subject = "🚨 New Device Login Attempt - SafeBank"
    content = f'''
    <p>We noticed a login attempt from a new device.</p>
    <p>If this was <strong>you</strong>, please confirm:</p>
    <p><a href="{yes_url}">✅ Yes, this is me</a></p>
    <br>
    <p>If this was <strong>not you</strong>, click below to block it:</p>
    <p><a href="{no_url}">❌ No, block this attempt</a></p>
    <br><p>This helps us keep your account secure.</p>
    '''
    send_email(email, subject, content, is_html=True)

def send_new_device_verification_email(to_email, link, device_info, ip):
    """Alternate version - call this only if link is externally generated"""
    subject = "🛡️ New Device Login - SafeBank"
    content = f'''
    <p>Hi,</p>
    <p>We detected a login attempt from a new device:</p>
    <ul>
        <li><strong>IP Address:</strong> {ip}</li>
        <li><strong>Device:</strong> {device_info}</li>
    </ul>
    <p>If this was you, click below to confirm and trust this device:</p>
    <p><a href="{link}">✅ Yes, this is me</a></p>
    <br>
    <p>If this was <strong>not you</strong>, we recommend changing your password immediately.</p>
    '''
    send_email(to_email, subject, content, is_html=True)

def send_generic_email(receiver_email, subject, body):
    """Send a simple custom plain text email"""
    send_email(receiver_email, subject, body)

# Test (manual run)
if __name__ == "__main__":
    test_email = "test@example.com"
    send_otp(test_email)
    print("✅ OTP sent for testing. Check inbox.")
