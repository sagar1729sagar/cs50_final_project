from flask import Flask, render_template, request, flash, redirect
import sqlite3
from helpers import check_email,create_email

app = Flask(__name__)
app.secret_key = 'CS50_final'




@app.route("/")
def index():
    # Get templates
    db = sqlite3.connect('emails.db')
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM template")
    rows = cursor.fetchall()
    return render_template("/index.html", rows=rows)


@app.route("/email", methods=["GET", "POST"])
def email():
   if request.method == "POST":
      option = request.form.get('template_id')
      variables = []
      receivers = []
      if option:
         # Get variables
         db = sqlite3.connect('emails.db')
         cursor = db.cursor()
         cursor.execute("SELECT * FROM variables WHERE template_id = ?", [option])
         variables = cursor.fetchall()  
         cursor.execute("SELECT * FROM receiver WHERE template_id = ?", [option])
         receivers = cursor.fetchall()
         db.close()
         print(variables)
         print(receivers)
         #Make dictionaries
         variables = [{'name':name, 'value':''} for _,name,_ in variables]
         receivers = [{'name': email_id, 'value': email_id, 'type':value} for _,email_id,value,_ in receivers]
         print(variables)
         print(receivers)
      return render_template('email.html', template_id=option, variables=variables, receivers=receivers)
   elif request.args.get('email_body'):
      print("Creatin started")
      create_email(request.args)
      return redirect("/")
   else :
      print(request.args)
      template_id = request.args.get('template_id')
      print("get params")
      print(template_id)
      #Get varaibles
      db = sqlite3.connect('emails.db')
      cursor = db.cursor()
      cursor.execute("SELECT * FROM variables WHERE template_id = ?", [template_id])
      variables = cursor.fetchall()  
      cursor.execute("SELECT * FROM receiver WHERE template_id = ?", [template_id])
      receivers = cursor.fetchall()
      cursor.execute("SELECT * FROM template WHERE id = ?", [template_id])
      body = cursor.fetchall()
      db.close()

      # #Change tuples to arrays
      variables = [{'name':name, 'value':request.args.get(name)} for _,name,_ in variables]
      receivers = [{'name': email_id, 'value': request.args.get(email_id), 'type':value} for _,email_id,value,_ in receivers]
      # variables = [[a,b,c] for a,b,c in variables]
      # receivers = [[a,b,c,d] for a,b,c,d in receivers]

      # #Update values with get variables
      # # variable_dict, receiver_dict
      # for variable in variables

      # Set preview text
      if body:
         body = body[0][1]
         for variable in variables:
            body = body.replace("'"+variable['name']+"'", variable['value'])
      
      return render_template('email.html', template_id= template_id, variables=variables, receivers=receivers, preview= body)


@app.route("/template", methods=["GET","POST"])
def template():
    if request.method == "POST":
        # Check fields
        variables = request.form.get('variables')
        print(variables)
        if variables:
           variables = variables.split(',')
           variables = [v.strip() for v in variables if v]
        print(variables)

        body = request.form.get('mail_body')
        print(body)
        if not body:
           flash("Email body text is required")
           return redirect('/template')
        
        signature = request.form.get('signature')

        send_to = request.form.get('sent_mail_id')
        print(send_to)
        if send_to:
           if not check_email(send_to):
              send_to = ""
        print(send_to)

        cc_to = request.form.get("cc_to")
        print(cc_to)
        if cc_to:
           cc_to = cc_to.split(';')
           cc_to = [c.strip() for c in cc_to if check_email(c)]
        print(cc_to)

        db = sqlite3.connect('emails.db')
        cursor = db.cursor()

        # Add template
        cursor.execute("INSERT INTO template (body) VALUES (?)", [body])
        db.commit()
        template_id = cursor.lastrowid
        print("Template id "+str(cursor.lastrowid))

        # Add variables
        if variables:
           for variable in variables:
              cursor.execute("INSERT INTO variables(name, template_id) VALUES(?,?)", [variable, template_id])
 
        print("Variables inserted")

        
        # Add Signature
        if signature:
           cursor.execute("INSERT INTO signature(text,template_id) VALUES(?,?)", [signature, template_id])

        # Add recipient
        if send_to:
           cursor.execute("INSERT INTO receiver(mail_id, type, template_id) VALUES (?,?,?)", [send_to, 1, template_id])

        

        # Add cc
        if cc_to:
           for cc in cc_to:
              print(cc)
              cursor.execute("INSERT INTO receiver(mail_id, type, template_id) VALUES (?,?,?)", [cc, 2, template_id])

        db.commit()
        db.close()  

        return redirect("/")
    else:
     return render_template("template.html")


if __name__ == '__main__':
    app.run()