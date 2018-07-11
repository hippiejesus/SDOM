import sys
import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

#python emailMe.py | address | subject | filename | password
#EG: python emailMe.py sdom.metrics@gmail.com testing test.csv sdope101

args = None

"""if len(args) < 4:
    print('Not enough arguments')
elif len(args) > 4:
    print('Too many arguments!')< """
def main(args):
    args.pop(0)
    print args[0]+','+args[1]+','+args[2]
    fromaddr = "sdom.metrics@gmail.com"
    toaddr = args[0]
    passwrd= args[3]
 
    msg = MIMEMultipart()
 
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = args[1]
 
    body = "Send request: "+str(datetime.datetime.now())
 
    msg.attach(MIMEText(body, 'plain'))
 
    filename = args[2]
    attachment = open("/home/pi/python/SDLabs/SDOM/CSV/"+args[2], "rb")
 
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
    msg.attach(part)
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, passwrd)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    return 0
    
if __name__=='__main__':
    args = sys.argv
    main(args)
