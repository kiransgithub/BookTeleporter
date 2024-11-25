import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.mime.base import MIMEBase
from email import encoders

#Email Constants
YAH="bookkeeper61611@yahoo.com"
yahoo_mail_pwd="b00kk33p3r2022"
yahoo_app_pwd="jlazkhixseoxzppo"
to = ['kiran.yaggadi@yahoo.com']
subject = "mail test with attachment"
text = "Check if you are able to access the attachment in this email"
files=["/Users/kirankumarchithaluri/BookTeleporter/Beginning Python.pdf"]
server = "smtp.mail.yahoo.com:587"

def send_mail(send_from, send_to, subject, text, attachments=None):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    for attachment in attachments or []:
        print("attachment: ",attachment)
        attachment = open(attachment, "rb")
        attachment = open(os.getcwd() + "/" + filename, "rb")
        filepart = MIMEBase('application', 'octet-stream')
        filepart.set_payload((attachment).read())
        encoders.encode_base64(filepart)
        filepart.add_header('Content-Disposition', "attachment; filename= %s" % attachment)
        msg.attach(filepart)

    email_session = smtplib.SMTP('smtp.mail.yahoo.com', 587)
    email_session.starttls()
    email_session.login(send_from, yahoo_app_pwd);
    email_session.sendmail(send_from, send_to, msg.as_string())
    email_session.quit()



fromMy="bookkeeper61611@yahoo.com"
yahoo_mail_pwd="b00kk33p3r2022"
yahoo_app_pwd="jlazkhixseoxzppo"
to = ['kiran.yaggadi@yahoo.com']
subject = "mail test with attachment"
text = "Check if you are able to access the attachment in this email"
files=["/Users/kirankumarchithaluri/BookTeleporter/Beginning Python.pdf"]
server = "smtp.mail.yahoo.com:587"


send_mail(fromMy,to,subject,text,files)