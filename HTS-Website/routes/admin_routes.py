
from flask import Flask, render_template, request,session, redirect, url_for, jsonify, Blueprint
import requests, json, base64, pymongo



adminapp = Blueprint('adminapp', __name__)

#-------------------------------------------Admin Routes-------------------------------------------------


@adminapp.route('/adminlogin', methods=["GET","POST"])
def adminlogin():
    error =""
    if request.method == 'POST':
        try:
            print(request.form['email'])
            session['email'] = request.form['email']
            
            PARAMS = {"email":request.form['email'],"pass":request.form['pass']} 
            headers = {'content-type': 'application/json'}
            print(type(PARAMS))
            r = requests.post(url = "http://127.0.0.1:5000" +url_for("backend.emp_login"), data = json.dumps(PARAMS),headers = headers) 
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

    return render_template('admin/adminlogin.html',error=error)


@adminapp.route('/adminDash')
def adminDash():
    if 'email' in session:
        user= session["email"]
        print(user)
        return render_template("admin/admin_dash.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))

@adminapp.route("/adminlogout")
def adminlogout():
    session.pop('email', None)
    return redirect(url_for('adminapp.adminlogin'))

@adminapp.route('/adminDash/addemp')
def adminDash_addemp():
    if 'email' in session:
        user= session["email"]
        return render_template("admin/add_emp.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    
@adminapp.route('/adminDash/add_application')
def adminDash_addapplication():
    if 'email' in session:
        user= session["email"]
        return render_template("admin/add_application.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))

@adminapp.route('/adminDash/add_file')
def adminDash_addfile():
    if 'email' in session:
        user= session["email"]
        return render_template("admin/add_file.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))

@adminapp.route('/adminDash/add_dept')
def adminDash_add_dept():
    if 'email' in session:
        user= session["email"]
        return render_template("admin/add_dept.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))    
    
    
    
    
    
@adminapp.route('/adminDash/search_file')
def adminDash_searchfile():
    if 'email' in session:
        user= session["email"]
        return render_template("admin/adminsearch.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    

@adminapp.route('/adminDash/processingfiles')
def adminDash_processingfiles():
    if 'email' in session:
        user= session["email"]
        return render_template("admin/adminprocessfiles.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    
@adminapp.route('/adminDash/delayedfiles')
def adminDash_delayedfiles():
    if 'email' in session:
        user= session["email"]
        return render_template("admin/admindelayedfiles.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    
@adminapp.route('/adminDash/completedfiles')
def adminDash_completedfiles():
    if 'email' in session:
        user= session["email"]
        return render_template("admin/admincompletedfiles.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    
@adminapp.route('/adminDash/employeeRatings')
def employeeRatings():
    if 'email' in session:
        user= session["email"]
        return render_template("admin/employee_ratings.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))

@adminapp.route('/adminDash/calender')
def calender():
    if 'email' in session:
        user= session["email"]
        return render_template("admin/add_holiday.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    
@adminapp.route('/adminDash/adminalert')
def adminalert():
    if 'email' in session:
        user= session["email"]
        return render_template("admin/adminalert.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))


@adminapp.route('/adminDash/dd')
def dd():
    if 'email' in session:
        user= session["email"]
        return render_template("admin/dd.html", user=user)
    else:
        return redirect(url_for("adminapp.adminlogin"))
#-------------------------------------------Admin Routes End-------------------------------------------------