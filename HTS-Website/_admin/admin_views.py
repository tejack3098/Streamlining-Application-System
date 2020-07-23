
from flask import Flask, render_template, request,session, redirect, url_for, jsonify
import requests, json, base64, pymongo

from . import adminapp



#-------------------------------------------Admin Routes-------------------------------------------------

@adminapp.route('/', methods=["GET","POST"])
@adminapp.route('/login', methods=["GET","POST"])
def adminlogin():
    error =""
    if request.method == 'POST':
        try:
            print(request.form['email'])
            session['email'] = request.form['email']
            
            PARAMS = {"email":request.form['email'],"pass":request.form['pass']} 
            headers = {'content-type': 'application/json'}
            print(type(PARAMS))
            r = requests.post(url = "http://127.0.0.1:5000" +url_for("backendapp.emp_login"), data = json.dumps(PARAMS),headers = headers) 
            data=json.loads(r.text)
            
            print(type(data))
            status=data['status']
            
            #print(session['dept_id'])
            if status==1:
                session['dept_id'] = data['message']['dept_id']
                print(session['dept_id']) 
                return redirect(url_for("adminapp.adminDash"))

            else:
                error="Invalid Credentials. Please try again."
        except:
            print("Exception occuered")
            raise

    return render_template('adminlogin.html',error=error)


@adminapp.route('/Dashboard')
def adminDash():
    if 'email' in session:
        user= session["email"]
        print(user)
        return render_template("admin_dash.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))

@adminapp.route("/logout")
def adminlogout():
    session.pop('email', None)
    return redirect(url_for('adminapp.adminlogin'))

@adminapp.route('/addemp')
def adminDash_addemp():
    if 'email' in session:
        user= session["email"]
        return render_template("add_emp.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    
@adminapp.route('/add_application')
def adminDash_addapplication():
    if 'email' in session:
        user= session["email"]
        return render_template("add_application.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))

@adminapp.route('/add_file')
def adminDash_addfile():
    if 'email' in session:
        user= session["email"]
        return render_template("add_file.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))

@adminapp.route('/add_dept')
def adminDash_add_dept():
    if 'email' in session:
        user= session["email"]
        return render_template("add_dept.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))    
    
    
    
    
    
@adminapp.route('/search_file')
def adminDash_searchfile():
    if 'email' in session:
        user= session["email"]
        return render_template("adminsearch.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    

@adminapp.route('/processingfiles')
def adminDash_processingfiles():
    if 'email' in session:
        user= session["email"]
        return render_template("adminprocessfiles.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    
@adminapp.route('/delayedfiles')
def adminDash_delayedfiles():
    if 'email' in session:
        user= session["email"]
        return render_template("admindelayedfiles.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    
@adminapp.route('/completedfiles')
def adminDash_completedfiles():
    if 'email' in session:
        user= session["email"]
        return render_template("admincompletedfiles.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    
@adminapp.route('/employeeRatings')
def employeeRatings():
    if 'email' in session:
        user= session["email"]
        return render_template("employee_ratings.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))

@adminapp.route('/calender')
def calender():
    if 'email' in session:
        user= session["email"]
        return render_template("add_holiday.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    
@adminapp.route('/alert')
def adminalert():
    if 'email' in session:
        user= session["email"]
        return render_template("adminalert.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))


@adminapp.route('/dd')
def dd():
    if 'email' in session:
        user= session["email"]
        return render_template("dd.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))
#-------------------------------------------Admin Routes End-------------------------------------------------