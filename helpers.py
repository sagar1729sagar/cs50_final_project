import re
import win32com.client
import pythoncom
import sqlite3

def check_email(email):  
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):  
        return True  
    return False


def create_email(data):
    print("Yay")
    print(data)
    db = sqlite3.connect('emails.db')
    cursor = db.cursor() 
    cursor.execute("SELECT * FROM receiver WHERE template_id = ?", [data.get('template_id')])
    receivers = cursor.fetchall()
    db.close()
    print(receivers)
    ol = win32com.client.Dispatch('Outlook.Application', pythoncom.CoInitialize())
    olmailitem = 0x0
    newmail = ol.CreateItem(olmailitem)
    newmail.Subject = data.get('email_subject') if data.get('email_subject') else ""
    senders = ";".join([data.get(ids) for _,ids,type,_ in receivers if type == 1 and data.get(ids)])
    ccs = ";".join([data.get(ids) for _,ids,type,_ in receivers if type == 2 and data.get(ids)])
    print(senders)
    print(ccs)
    newmail.To = senders
    newmail.CC = ccs
    newmail.Body= data.get('email_body')
    newmail.Display()
    