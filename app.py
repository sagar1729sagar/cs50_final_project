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
    db.close()
    return render_template("/index.html", rows=rows)


@app.route("/happy")
def happy():
   return render_template('happy.html')


@app.route("/save/<id>", methods=["POST","GET"])
def save(id):
   print("uo")
   print(id)
   #todo del
   print(request.form)
   variables = request.form.get('variables')
   print(variables)
   if variables:
      variables = variables.split(',')
      variables = [v.strip() for v in variables if v]
   print(variables)

   subject = request.form.get('mail_subject')
   print('subject')
   print(subject)

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
   cursor.execute("INSERT INTO template (body, subject) VALUES (?,?)", [body, subject])
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


   cursor.execute("DELETE FROM variables WHERE template_id=?",[id])
   cursor.execute("DELETE FROM template WHERE id=?",[id])
   cursor.execute("DELETE FROM signature WHERE template_id=?",[id])
   cursor.execute("DELETE FROM receiver WHERE template_id=?",[id])
   db.commit()
   db.close()  

   return redirect("/")


@app.route("/edit")
def edit():
   # Get templates
    db = sqlite3.connect('emails.db')
    cursor = db.cursor() 
    cursor.execute("SELECT * FROM template")
    rows = cursor.fetchall()
    db.close()
    return render_template("/edit.html", rows=rows)


@app.route('/delete/<id>')
def delete(id):
   db = sqlite3.connect('emails.db')
   cursor = db.cursor()
   cursor.execute('DELETE FROM receiver WHERE  template_id = ?',[id])
   cursor.execute('DELETE FROM signature WHERE  template_id = ?',[id])
   cursor.execute('DELETE FROM template WHERE  id = ?',[id])
   cursor.execute('DELETE FROM variables WHERE  template_id = ?',[id])
   db.commit()
   db.close()
   return redirect("/edit")


@app.route('/edit_template/<id>')
def edit_template(id):
   db = sqlite3.connect('emails.db')
   cursor = db.cursor()

   cursor.execute('SELECT * FROM variables WHERE template_id = ?',[id])
   variables = cursor.fetchall()
   variables = ",".join([name for _,name,_ in variables]) if variables else ''

   cursor.execute('SELECT * FROM template WHERE id = ?',[id])
   email = cursor.fetchall()
   subject = email[0][2] if email[0][2] else ''
   body = email[0][1]
   print(email)

   cursor.execute('SELECT * FROM signature WHERE template_id = ?',[id])
   signature = cursor.fetchall()
   signature = signature[0][1] if signature else ''

   cursor.execute('SELECT * FROM receiver WHERE  template_id= ?', [id])
   mail_ids = cursor.fetchall()
   sends = ";".join([email_id for _,email_id,value,_ in mail_ids if value == 1]) if mail_ids else ''
   ccs = ";".join([email_id for _,email_id,value,_ in mail_ids if value == 2]) if mail_ids else ''

   db.close()
   return render_template("/edit_template.html", variables=variables, subject=subject, body=body, signature=signature, sends=sends, ccs=ccs, id=id)

@app.route("/email", methods=["GET", "POST"])
def email():
   if request.method == "POST":
      option = request.form.get('template_id')
      print("option")
      print(option)
      variables = []
      receivers = []
      signature = ''
      if option:
         # Get variables
         db = sqlite3.connect('emails.db')
         cursor = db.cursor()
         cursor.execute("SELECT * FROM variables WHERE template_id = ?", [option])
         variables = cursor.fetchall()  
         cursor.execute("SELECT * FROM receiver WHERE template_id = ?", [option])
         receivers = cursor.fetchall()
         cursor.execute("SELECT * FROM signature WHERE template_id = ?", [option])
         signature = cursor.fetchall()
         db.close()
         print(variables)
         print(receivers)
         #Make dictionaries
         variables = [{'name':name, 'value':''} for _,name,_ in variables]
         receivers = [{'name': email_id, 'value': email_id, 'type':value} for _,email_id,value,_ in receivers]
         signature = signature[0][1] if signature else ''
         print(variables)
         print(receivers)
         print(signature)
      return render_template('email.html', template_id=option, variables=variables, receivers=receivers, signature=signature)
   elif request.args.get('email_body'):
      print("Creatin started")
      create_email(request.args)
      return redirect("/happy")
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
      signature = request.args.get('signature')
      # variables = [[a,b,c] for a,b,c in variables]
      # receivers = [[a,b,c,d] for a,b,c,d in receivers]

      # #Update values with get variables
      # # variable_dict, receiver_dict
      # for variable in variables

      # Set preview text
      print('body')
      print(body)
      if body:
         subject = body[0][2]
         body = body[0][1]
         for variable in variables:
            body = body.replace("'"+variable['name']+"'", variable['value'])
            if subject:
               subject = subject.replace("'"+variable['name']+"'", variable['value'])
            if signature:
               signature = signature.replace("'"+variable['name']+"'", variable['value'])
      else:
         body=''
         subject=''
      if signature:
         body = body + '\n\n\n' + signature
      
      return render_template('email.html', template_id= template_id, variables=variables, receivers=receivers, preview= [body, subject])


@app.route("/template", methods=["GET","POST"])
def template():
    print(request.args)
    print(request.form)
    if request.method == "POST":
        # Check fields
        print(request.form)
        variables = request.form.get('variables')
        print(variables)
        if variables:
           variables = variables.split(',')
           variables = [v.strip() for v in variables if v]
        print(variables)

        subject = request.form.get('mail_subject')
        print('subject')
        print(subject)

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
        cursor.execute("INSERT INTO template (body, subject) VALUES (?,?)", [body, subject])
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