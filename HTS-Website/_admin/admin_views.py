
from flask import Flask, render_template, request,session, redirect, url_for, jsonify
import requests, json, base64, pymongo

from . import adminapp



#-------------------------------------------Admin Routes-------------------------------------------------

@adminapp.route('/', methods=["GET","POST"])
@adminapp.route('/login', methods=["GET","POST"])
def adminlogin():
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
        
          
            if status==1:
                session[email] = email
                print("====================================================================")
                print(session.keys())
                print("====================================================================")
                return redirect(url_for("adminapp.adminDash", email = email))
            else :
                error="Invalid Credentials. Please try again."
        except:
            print("Exception occuered")
            raise
    return render_template('adminlogin.html',error=error)


@adminapp.route('/Dashboard/<email>')
def adminDash(email):
    if email in session:
        return render_template("admin_dash.html", email=email)
    else:
        return redirect(url_for("adminapp.adminlogin"))

@adminapp.route('/generateReport/<email>',methods=['GET','POST'])
def generateReport(email):
    if email in session:
        return render_template("report_generate.html",email=email)
    else:
        return redirect(url_for("adminapp.adminlogin"))

@adminapp.route("/logout/<email>")
def adminlogout(email):
    session.pop(email, None)
    return redirect(url_for('adminapp.adminlogin'))

@adminapp.route('/addemp/<email>')
def adminDash_addemp(email):
    if email in session:
        return render_template("add_emp.html", email=email)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    
@adminapp.route('/add_application/<email>')
def adminDash_addapplication(email):
    if email in session:
        return render_template("add_application.html", email=email)
    else:
        return redirect(url_for("adminapp.adminlogin"))

@adminapp.route('/add_file/<email>')
def adminDash_addfile(email):
    if email in session:
        return render_template("add_file.html", email=email)
    else:
        return redirect(url_for("adminapp.adminlogin"))

@adminapp.route('/add_dept/<email>')
def adminDash_add_dept(email):
    if email in session:
        return render_template("add_dept.html", email=email)
    else:
        return redirect(url_for("adminapp.adminlogin"))    
    
    
    
    
    
@adminapp.route('/search_file/<email>')
def adminDash_searchfile(email):
    if email in session:
        return render_template("adminsearch.html", email=email)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    

@adminapp.route('/processingfiles/<email>')
def adminDash_processingfiles(email):
    if email in session:
        return render_template("adminprocessfiles.html", email=email)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    
@adminapp.route('/delayedfiles/<email>')
def adminDash_delayedfiles(email):
    if email in session:
        return render_template("admindelayedfiles.html", email=email)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    
@adminapp.route('/completedfiles/<email>')
def adminDash_completedfiles(email):
    if email in session:
        return render_template("admincompletedfiles.html", email=email)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    
@adminapp.route('/employeeRatings/<email>')
def employeeRatings(email):
    if email in session:
        return render_template("employee_ratings.html", email=email)
    else:
        return redirect(url_for("adminapp.adminlogin"))

@adminapp.route('/employeesearch/<email>')
def employeesearch(email):
    if email in session:
        return render_template("admin_employee_search.html", email=email)
    else:
        return redirect(url_for("adminapp.adminlogin"))

@adminapp.route('/calender/<email>')
def calender(email):
    if email in session:
        return render_template("add_holiday.html", email=email)
    else:
        return redirect(url_for("adminapp.adminlogin"))
    
@adminapp.route('/alert/<email>')
def adminalert(email):
    if email in session:
        return render_template("adminalert.html", email=email)
    else:
        return redirect(url_for("adminapp.adminlogin"))


@adminapp.route('/dd/<email>')
def dd(email):
    if email in session:
        return render_template("dd.html", email=email)
    else:
        return redirect(url_for("adminapp.adminlogin"))
#-------------------------------------------Admin Routes End-------------------------------------------------