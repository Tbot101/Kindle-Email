from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from os import path
import smtplib
import shutil
import requests.auth


source = r'\Reading Books'  # name of folder where books are stored is reading books
print(os.listdir('Reading Books'))
booklist = []
newbooknames = []
for filename in os.listdir("/Reading Books"):
    exists = re.findall('.pdf', filename)
    exists1 = re.findall('.PDF', filename)
    exists2 = re.findall('.azw3', filename)
    if exists:
        booklist.append(filename)
    elif exists1:
        booklist.append(filename)
    elif exists2:
        booklist.append(filename)
    else:
        pass
print(booklist)

for book in booklist:
    newname = re.sub('z-lib.org', '', book)
    newname1 = re.sub('.epub', '', newname)
    newname2 = re.sub('.mobi', '', newname1)
    newname3 = re.sub(r' \(\)', '', newname2)
    newbooknames.append(newname3)
    os.rename(path.join(source, book), path.join(source, newname3))
    print(newbooknames)

    def send_mail():
        mail_content = '''Hello,
    Please find attached the kindle pdf.
        '''
        # The mail addresses and password
        sender_address = 'INSERT EMAIL'
        sender_pass = 'EMAIL PASSWORD'
        receiver_address = 'KINDLE EMAIL'

        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        if '.azw3' in newname3:
            message['Subject'] = 'email'
        else:
            message['Subject'] = 'convert'

        # The subject line
        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))

        attach_file_name = '/Reading Books/%s' % newname3

        # Open the file as binary mode
        attach_file = open(attach_file_name, 'rb')
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())

        encoders.encode_base64(payload)  # encode the attachment

        # add payload header with filename
        payload.add_header('Content-Disposition',
                           "attachment; filename= %s" % newname3)
        message.attach(payload)
        text = message.as_string()

        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        # login with mail_id and password
        session.login(sender_address, sender_pass)

        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')

    send_mail()

    destination = r'\Sent Books'  # move pdf to this folder after sent to Kindle
    shutil.move(path.join(source, newname3), destination)
    print("Moved the book to different folder")
print("Finished sending all books to kindle!")
