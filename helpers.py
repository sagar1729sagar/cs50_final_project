import re
import win32com.client
import pythoncom

def check_email(email):  
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):  
        return True  
    return False


def create_email(data):
    print("Yay")
    ol = win32com.client.Dispatch('Outlook.Application', pythoncom.CoInitialize())
    olmailitem = 0x0
    newmail = ol.CreateItem(olmailitem)
    newmail.Subject = 'Testing Mail'
    newmail.To = 'xyz@gmail.com'
    newmail.CC = 'xyz@gmail.com'
    newmail.Body= 'Hello, this is a test email to showcase how to send emails from Python and Outlook.'
    newmail.Display()