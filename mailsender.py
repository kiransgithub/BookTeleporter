import mimetypes




#Constants
SERVER_ADDRESS = "smtp.mail.yahoo.com"
SERVER_PORT = 587
SENDER_EMAIL_ADDRESS = "bookkeeper61611@yahoo.com"
SENDER_APP_EMAIL_PASSWORD = "jlazkhixseoxzppo"
RECIPIENT_EMAIL = "kiran.yaggadi@yahoo.com"



fromMy="bookkeeper61611@yahoo.com"
yahoo_mail_pwd="b00kk33p3r2022"
yahoo_app_pwd="jlazkhixseoxzppo"
to = ['kiran.yaggadi@yahoo.com']
subject = "mail test with attachment"
text = "Check if you are able to access the attachment in this email"
files=["/Users/kirankumarchithaluri/BookTeleporter/Beginning Python.pdf"]
server = "smtp.mail.yahoo.com:587"

filename = 'Beginning Python.pdf'
path = f'{os.getcwd()}/{filename}'

# Guess the content type based on the file's extension.
ctype, encoding = mimetypes.guess_type(path)
if ctype is None or encoding is not None:
    ctype = 'application/octet-stream'
maintype, subtype = ctype.split('/', 1)

with open(path, 'rb') as fp:
    msg.add_attachment(fp.read(), maintype=maintype, subtype=subtype, filename=filename)


import smtplib
import ssl

# Create a SSLContext object with default settings.
context = ssl.create_default_context()

with smtplib.SMTP(SERVER_ADDRESS, SERVER_PORT) as smtp:
    smtp.ehlo()  # Say EHLO to server
    smtp.starttls(context=context)  # Puts the connection in TLS mode.
    smtp.ehlo()
    smtp.login(SENDER_EMAIL_ADDRESS, SENDER_APP_EMAIL_PASSWORD)
    smtp.send_message(msg)  # Auto detects the sender and recipient from header



from email.message import EmailMessage

msg = EmailMessage()

msg['Subject'] = "My Custom Subject"
msg['From'] = EMAIL_ADDRESS
msg['To'] = RECIPIENT_EMAIL

msg.set_content('Hello World')

msg.add_alternative("""
<p>
    <h1>My Custom Title</h1>
    Hello <strong>World</strong>
</p>
""", subtype='html')