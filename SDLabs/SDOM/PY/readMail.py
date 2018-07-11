import sys
import smtplib
import time
import imaplib
import email
import emailMe
import subprocess
import SQLinterface

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "sdom.metrics" + ORG_EMAIL
FROM_PWD = "sdope101"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

def readmail():
    pass
    
class connection:
    def __init__(self):
        self.mail = None
        self.found = False
        self.login()
        self.querySubject()
        self.logout()
        
    def login(self):
        self.mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        self.mail.login(FROM_EMAIL,FROM_PWD)
        self.mail.select('inbox')
        
    def logout(self):
        self.mail.close()
        self.mail.logout()
        
    #Return list of compatible emails with subject 'request'
    def querySubject(self):
        type, data = self.mail.search(None, 'ALL')
        mail_ids = data[0]
        id_list = mail_ids.split()
        
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        
        for i in range(latest_email_id,first_email_id,-1):
            typ, data = self.mail.fetch(i, '(RFC822)')
            
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    payload = msg.get_payload()
                    email_body = payload[0].get_payload(decode = True)
                    """print 'From: '+email_from+'\n'
                    print 'Subject: '+email_subject+'\n'
                    print 'Body: '+email_body+'\n'"""
                    
                    if email_subject == 'request':
                        print('Found request...')
                        self.found = True
                        
                        splitBody = email_body.split()
                        
                        args = []
                        
                        if splitBody[0] == 'runs':
                            print('Resolving...')
                            args.append('emailMe.py')
                            args.append(str(email_from))
                            args.append('testing')
                            args.append('test.csv')
                            args.append(str(FROM_PWD))
                        else:
                            try:
                                back = SQLinterface.csvMe(str(email_body))
                                if back != False:
                                    args.append('emailMe.py')
                                    args.append(str(email_from))
                                    args.append('requested metrics enclosed')
                                    args.append(back)
                                    args.append(str(FROM_PWD))
                                else:
                                    print('failed to create csv')
                                    return
                            except:
                                return
                        
                        email_completed = emailMe.main(args)
                        if email_completed == 0:
                            print('Table sent')
                            try:    
                                self.mail.store(i, '+FLAGS', '\\Deleted')
                                self.mail.expunge()
                                print('Request marked for deletion...')
                            except:
                                print('Error: '+str(e))
   
if __name__=='__main__':
    print('Starting server...')
    while True:
        con = connection()
        print('Found: '+str(con.found))
        print('Cycling...\n\n')

        
        
        
        
