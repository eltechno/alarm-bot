#!/usr/bin/env python
""" 

Alarm-Bot

Longer description of this module.

A small python script to monitor your Linux FS and report any issues via email using gmail accounts

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.

author: Paulo Alvarado
contact: paulo@alvarado.com.gt
"""

import subprocess
import smtplib
import socket
from email.mime.text import MIMEText

hostname = socket.gethostname()

def report_via_email():
""" set all the information to create the email body and credentials """
    msg = MIMEText(f'Server {hostname}, running out of disk space')
    msg["Subject"] = "Low disk space warning less than 80%"
    msg["From"] = "your_gmail_account@gmail.com"
    msg["To"] = "sysadmin_email@company.com"
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("gmail_username", "password")
        server.sendmail("your_gmail_account@gmail.com","sysadmin_email@company.com",msg.as_string())
        server.quit()

"""set the trigger """
threshold = 80

""" se the partition to check"""
partition = "/"

def check_once():
"""check the fs space and make decision for send or not the alarm email """
    df = subprocess.Popen(["df","-h"], stdout=subprocess.PIPE)
    for line in df.stdout:
        splitline = line.decode().split()
        if splitline[5] == partition:
            if int(splitline[4][:-1]) > threshold:
                report_via_email()
                print("email sent")
check_once()
