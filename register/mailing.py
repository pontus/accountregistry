import smtplib

def send(to, message):
    p = smtplib.SMTP('127.0.0.1')
    p.ehlo()
    p.mail('webmaster@bils.se')
    p.rcpt(to)
    p.data(message)
    p.close()
