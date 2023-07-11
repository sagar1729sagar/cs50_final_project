# cs50_final_project
# My email templates

Url - **********

This app  allows its users to create an email template and then use it to generate a drafted outlook email.This is helpful for people who are to send same email multiple times periodically with small change in details. Instead of typing the same email every time, they can just use a template they created, change a few details and send the email.

## What can I do here?
    User can define an email template with default values for body of email, signature, emails ids of perple to which that email can be sent.
    User also can define placeholders or variables that need to change based on user input, everytime the email is drafted using that template.
    Users can define multiple templates and use them any number of times by directly selecting them from home page.

# How to I do it?
    1. ***Run your app***
            Double click on the app file. This will run a local server and it shows an address which is to be copied in browser or control clicked to open the app

    2. ***Create a template***
        An email template can be created by clicking on  create template button on homepage or through menu in navigational bar.
        Once the creation page is open, user is prompted to enter several details

        a. _Variables_ - These are the names or values which users have to change or insert in email body evertytime the email is drafted.All the variable names are to be written here seperated by commas(,). This can  be left blank if there are no values that change in your email.
        Example : name, company_name

        b. _Subject_ - Here subject of the email has to be given. For variables, values that change everytime email is drafted, variable names that are entered in previous box are to be given, enclosing them in single quotes. This text field is can be left blank

        c._Email body_ - Here body of the email has to be given. For variables, values that change everytime email is drafted, variable names that are entered in previous box are to be given, enclosing them in single quoted
        Example : Hello 'name' from 'company_name'
                  Welcome to our group
                  blah blah blah
                   .........

        d. _Signature_ - Email signature that is to be used at the end of the email has to be given here. This text field is can be left blank

        f. _Send address_ - Email address of the person to whom email has to be sent everytime can be given here. This text field is can be left blank

        g. _CC addresses_ - Email addresses of the persons to whom carbon copies (cc) of email has to be sent everytime can be given here. This text field is can be left blank. Multiple email addresses can be given  here. They have to be seperated by semi-columns(;). Invalid formats are automatically discarded.
        Example : cc1@email.comcc2@email.com;cc3@email.com

    Once all the information is verified, clicking on create template button will create the user template and redirect user to homepage.

    3. ***Select a template***
        User can select the template they need to use from home page.
        On homepage, all the user created templates are displayed and one of them can be selected by clicking on the radio button to the left of it and procced to creating email draft by clicking on create email button

    4. ***Edit your information***
        In page you are presented with all the information that was given during template creating. User can edit any of them if they like, as a one time measure. The changes in information doesnot effect the original template created by user. User can also provide values to the variables here. By cliking on preview button, user is reditected to preview page.

    5. ***Preview your email***
        Here you can see the subject and body of the email where variables replaced with values provided by user on edit page. User can edit the subject and body here as per their requirement. This also does not effect the original template created.

    6. ***Create a draft***
        By clicking create mail button, an outlook email will open with values that are as defined in the template. Just verify them once angain and press send to send your email


That’s it . That is how you can easily send the same boring mail that you type everyday with minimal effort, using this app
Thank you for your time
