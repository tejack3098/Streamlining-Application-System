from flask import Flask, render_template, request,session, redirect, url_for, jsonify, Blueprint
import requests, json, base64, pymongo

empapp = Blueprint('empapp', __name__)


#-------------------------------------------Emp Routes-------------------------------------------------------


@empapp.route('/emplogin', methods=["GET","POST"])
def emplogin():
    error= ""
    if request.method == 'POST':
        try:
            print(request.form['email'])
            session['email'] = request.form['email']
            PARAMS = {"email":request.form['email'],"pass":request.form['pass']} 
            headers = {'content-type': 'application/json'}
            print(type(PARAMS))
            r = requests.post(url = "http://127.0.0.1:5000" +url_for("backend.emp_login"), data = json.dumps(PARAMS),headers = headers) 
            data=json.loads(r.text)
            
            print(data)
            status=data['status']
            print(status)
            #print(session['dept_id'])
            if status==1:
                session['dept_id'] = data['message']['dept_id']
                print(session['dept_id'])
                return redirect(url_for("empapp.empDash"))
            else :
                error="Invalid Credentials. Please try again."
        except:
            print("Exception occuered")
            raise
    return render_template('emp/emplogin.html',error=error)


@empapp.route('/empDash')
def empDash():
    if 'email' in session:
        user= session["email"]
        dept_id= session['dept_id']
        print("Emp -----"+dept_id)
        return render_template("emp/emp_dash.html", user=user,dept_id=dept_id)
    else:
        return redirect(url_for("empapp.emplogin"))


@empapp.route("/emplogout")
def emplogout():
    session.pop('email', None)
    return redirect(url_for('empapp.emplogin'))


@empapp.route('/empDash/workStatus')
def empDash_workStatus():
    if 'email' in session:
        user= session["email"]
        dept_id= session['dept_id']
        return render_template("emp/empwork.html", user=user,dept_id=dept_id)
    else:
        return redirect(url_for("empapp.emplogin"))
    
@empapp.route('/empDash/empnotification')
def empDash_empnotification():
    if 'email' in session:
        user= session["email"]
        dept_id= session['dept_id']
        return render_template("emp/empnotification.html", user=user,dept_id=dept_id)
    else:
        return redirect(url_for("empapp.emplogin"))

@empapp.route('/empProfile')
def empProfile():
    if 'email' in session:
        user= session["email"]
        dept_id= session['dept_id']
        return render_template("emp/emp_profile.html", user=user,dept_id=dept_id)
    else:
        return redirect(url_for("empapp.emplogin"))
#-------------------------------------------Emp Routes End--------------------------------------------------

