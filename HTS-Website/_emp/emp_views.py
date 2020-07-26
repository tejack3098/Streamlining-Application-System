from flask import Flask, render_template, request,session, redirect, url_for, jsonify
import requests, json, base64, pymongo


from . import empapp

#-------------------------------------------Emp Routes-------------------------------------------------------

@empapp.route('/', methods=["GET","POST"])
@empapp.route('/login', methods=["GET","POST"])
def emplogin():
    error= ""
    if request.method == 'POST':
        try:
            email = request.form['email']
            PARAMS = {"email":email,"pass":request.form['pass']} 
            headers = {'content-type': 'application/json'}
            print(type(PARAMS))
            r = requests.post(url = "http://127.0.0.1:5000" +url_for("backendapp.emp_login"), data = json.dumps(PARAMS),headers = headers) 
            data=json.loads(r.text)
           
            status=data['status']
            dept_id = data['message']['dept_id']
          
            if status==1:
                session[email] = email
                session[email[:-10]+'_dept_id'] = dept_id
                print("====================================================================")
                print(session.keys())
                print("====================================================================")
                return redirect(url_for("empapp.empDash", email = email, dept_id = dept_id ))
            else :
                error="Invalid Credentials. Please try again."
        except:
            print("Exception occuered")
            raise
    return render_template('emplogin.html',error=error)


@empapp.route('/Dashboard/<email>')
def empDash(email):
    if email in session:
        return render_template("emp_dash.html", email=email)
    else:
        return redirect(url_for("empapp.emplogin"))


@empapp.route("/logout/<email>")
def emplogout(email):
    session.pop(email, None)
    session.pop(email[:-10]+'_dept_id', None)
    return redirect(url_for('empapp.emplogin'))


@empapp.route('/workStatus/<email>')
def empworkStatus(email):
    if email in session:
        return render_template("empwork.html", email=email)
    else:
        return redirect(url_for("empapp.emplogin"))
    

@empapp.route('/Profile/<email>')
def empProfile(email):
    if email in session:
        return render_template("emp_profile.html", email=email)
    else:
        return redirect(url_for("empapp.emplogin"))
#-------------------------------------------Emp Routes End--------------------------------------------------

