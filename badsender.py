import argparse
import os
import platform
import time
import smtplib
from getpass import getpass
from email.message import EmailMessage
import data

parser = argparse.ArgumentParser(description='Send logs from Valhala or Artillery to your intel inbox', usage='%(prog)s [honeypot] LogPath time')
parser.add_argument('honeypot', type=str, choices=['valhala', 'artillery'])
parser.add_argument('logpath', help='Log path used for save log text file from valhala')
parser.add_argument('interval', type=int, help='Time between logs (secs)')
args = parser.parse_args()
honeypot = args.honeypot
logpath = args.logpath
interval = args.interval

smtp_server = data.smtp_server
port = data.port
sender_email = data.sender_email
receiver_email = data.receiver_email
password_email = getpass("Email Password:")

def send_mail(message, password):

    try:
        msg = EmailMessage()
        msg.set_content(message)

        msg['Subject'] = honeypot + ":" + platform.node()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        
        server = smtplib.SMTP_SSL(smtp_server, port)
        server.ehlo()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong",ex)
        exit()        

def honeypot_valhala():

    with open(get_file(), errors="ignore") as f:
        lines = f.readlines()
        message = ""
        for line in lines:
            message = message + line

    message = "".join(char for char in message if 31 < ord(char) < 127 or char in "\n\r")
    
    return message


def get_file():

        logdir = os.listdir(logpath)

        if len(logdir) == 0:
            return False
        else: 
            logfile = logpath + logdir[0]
            return logfile


if __name__ == "__main__":

    if honeypot == 'valhala':

        while True and (interval > 120):
            if get_file() == False:
                print("No new logs since last update\n...")
                time.sleep(interval)
                continue
            else:
                send_mail(honeypot_valhala(), password_email)
                os.remove(get_file())
                time.sleep(interval)
        exit("Interval must be at least 120s")
