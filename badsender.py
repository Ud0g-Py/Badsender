import argparse
import os
import platform
import time
import smtplib
from getpass import getpass
from email.message import EmailMessage

parser = argparse.ArgumentParser(description='Send logs from Valhala or Artillery to your intel inbox', usage='%(prog)s [honeypot] LogPath time')
parser.add_argument('honeypot', type=str, choices=['valhala', 'artillery'])
parser.add_argument('logpath', help='Log path used for save log text file from valhala')
parser.add_argument('interval', type=int, help='Time between logs (secs)')
args = parser.parse_args()
honeypot = args.honeypot
logpath = args.logpath
interval = args.interval

smtp_server = getpass("SMTP Server:")
port = getpass("Port (default 465):")
sender_email = getpass("From:")
receiver_email = getpass("To:")
password = getpass("Email Password:")

def send_mail(message):

    try:

        msg = EmailMessage()
        msg.set_content(message)

        msg['Subject'] = platform.node()
        msg['From'] = sender_email
        msg['To'] = receiver_email

        server = smtplib.SMTP_SSL(smtp_server, port)
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()

    except Exception as ex:

        print(ex)

def honeypot_valhala():

    logdir = os.listdir(logpath)
    logfile = logpath + logdir[0]

    with open(logfile) as f:

        lines = f.readlines()
        message = ""
        for line in lines:
            message = message + line

    os.remove(logfile)

    message = "".join(char for char in message if 31 < ord(char) < 127 or char in "\n\r")

    return message

if __name__ == "__main__":

    if honeypot == 'valhala':

        while True and interval > 30:
            send_mail(honeypot_valhala())
            time.sleep(interval)
        exit("Interval must be at least 30s")