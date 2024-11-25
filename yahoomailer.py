import smtplib

fromMy="bookkeeper61611@yahoo.com"
yahoo_mail_pwd="b00kk33p3r2022"
yahoo_app_pwd="jlazkhixseoxzppo"
to = 'kiran.yaggadi@yahoo.com'

# fromMy = 'yourMail@yahoo.com' # fun-fact: from is a keyword in python, you can't use it as variable, did abyone check if this code even works?
# to  = 'SomeOne@Example.com'
subj='TheSubject'
date='2/1/2010'
message_text='Hello Or any thing you want to send'

msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( fromMy, to, subj, date, message_text )


# yahoo_sender_email="bookkeeper61611@yahoo.com"
# yahoo_mail_pwd="b00kk33p3r2022"
# yahoo_app_pwd="jlazkhixseoxzppo"
# receiver_address = 'kiran.yaggadi@yahoo.com'

username = str(fromMy)  
password = str(yahoo_app_pwd)  

try :
    server = smtplib.SMTP("smtp.mail.yahoo.com",587)
    server.starttls() #enable security
    server.login(username,password)
    server.sendmail(fromMy, to,msg)
    server.quit()    
    print('ok the email has sent')
except Exception as e:
    print('can\'t send the Email : ',e)


