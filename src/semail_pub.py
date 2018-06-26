import smtplib

def send_email(subject,content):
    acc = input("Please enter your email account: ")
    psw = input("Please enter the password: ")

    content = "Subject:{}\n\n".format(subject) + content

    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()

    mail.starttls()
    mail.login(acc,psw)
    mail.sendmail(acc,acc,content)
    mail.close()
