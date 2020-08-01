from flask import Flask, render_template, request,session, redirect, url_for, jsonify
import requests, json, base64, pymongo
from datetime import datetime
from datetime import timedelta
import calendar, pickle
from flask_cors import CORS
from barcode import generate
from barcode.writer import ImageWriter
import qrcode
from qrcode.image.pure import PymagingImage
from . import backendapp

iwriter = ImageWriter()



#--------------------------------------------Back-End Starts-----------------------------------------------------

'''ML MODEL'''
pickle_file=open("model/DecisionTreeModel.pickle",'rb')
mlModel = pickle.load(pickle_file)
deptToNumber= {"01":1,"02":2,"03":3,"04":4,"05":5,"06":6}
appToNumber = {"PAN":1,"VID":2,"DLC":3,"ADC":4,"LON":5,"PPT":6}
'''ML MODEL'''

'''Quarter'''
quarterDetails = {"1":[1,3],"2":[4,6],"3":[7,9],"4":[10,12]}
'''Quarter'''

'''FILE COMPLAIN MESSAGE'''
file_complain_message="{} has not received File: {} sent from {} at {} !"
'''FILE COMPLAIN MESSAGE'''

try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
except:
    print("MongoDB Connection error")
    myclient = None
    raise
try:
    filetracker = myclient["filetracker"]
except:
    print("MongoDB error: DB might not exist")
    filetracker = None
try:
    files = filetracker["files"]
except:
    print("MongoDB error: files Table might not exist")
    files = None
try:
    applications = filetracker["applications"]
except:
    print("MongoDB error: files Table might not exist")
    applications = None
try:
    emp_data = filetracker["emp_data"]
except:
    print("MongoDB error: emp_data Table might not exist")
    emp_data=None
try:
    emp_stats = filetracker["emp_stats"]
except:
    print("MongoDB error: emp_stats Table might not exist")
    emp_stats=None

try:
    dept = filetracker["dept"]
except:
    print("MongoDB error: dept Table might not exist")
    dept=None

try:
    estimateTime = filetracker["estimateTime"]
except:
    print("MongoDB error: estimateTime Tbale might not exist")
    estimateTime = None
try:
    notifications = filetracker["notifications"]
except:
    print("MongoDB error: notifications Table might not exist")
    notifications=None

try:
    holidays = filetracker["holidays"]
except:
    print("MongoDB error: holidays Table might not exist")
    holidays=None
try:
    adminInbox = filetracker["adminInbox"]
except:
    print("MongoDB error: adminInbox Table might not exist")
    adminInbox = None

    
def chk_db():
    if myclient == None:
        #Connection error
        response = {"status": 3, "message": "MongoDB connection error"}
        return response
    elif filetracker == None:
        #DB error
        response = {"status": 3, "message": "MongoDB error: DB might not exist"}
        return response
    elif files == None:
        #Table error
        response = {"status": 3, "message": "MongoDB error: Files Table might not exist"}
        return response
    elif applications == None:
        # Table error
        response = {"status": 3, "message": "MongoDB error: applications Table might not exist"}
        return response
    elif dept == None:
        # Table error
        response = {"status": 3, "message": "MongoDB error: Dept Table might not exist"}
        return response
    elif emp_data == None:
        # Table error
        response = {"status": 3, "message": "MongoDB error: emp_data Table might not exist"}
        return response
    elif emp_stats == None:
        # Table error
        response = {"status": 3, "message": "MongoDB error: emp_stats Table might not exist"}
        return response
    elif estimateTime == None:
        # Table error
        response = {"status": 3, "message": "MongoDB error: estimateTime Table might not exist"}
        return response
    elif notifications == None:
        # Table error
        response = {"status": 3, "message": "MongoDB error: notification Table might not exist"}
        return response
    elif holidays == None:
        # Table error
        response = {"status": 3, "message": "MongoDB error: holidays Table might not exist"}
        return response
    elif adminInbox == None:
        # Table error
        response = {"status": 3, "message": "MongoDB error: adminInbox Table might not exist"}
        return response
    else:
        response ={"status":1,"message":"All good !"}
        return response

r = chk_db()

if r["status"]==3:
    print(r["message"])
    exit()
else:
    print(r["message"])

del(r)

@backendapp.route("/")
def index():
    return "SIKKIM is the only truth right now!"


@backendapp.route("/add_application",methods=["GET","POST"])
def add_application():
    if request.method == "POST":
        if "application/x-www-form-urlencoded" in request.headers["Content-Type"]:
            postData = request.form
        else:
            postData = request.get_json()
        print("postData \n {}".format(postData))
        appname = postData["appname"]
        appID = postData["appid"]
        dept_ID = postData.getlist("dept_id[]")
        print("dept_ID: {} \n value : {}".format(type(dept_ID),dept_ID))
        no_of_days = postData.getlist("no_of_days[]")
        print("no_of_days: {} \n value : {}".format(type(no_of_days), no_of_days))

        stageList=[]
        for i in range(len(dept_ID)):
            stageList.append({"dept_id":dept_ID[i],"no_of_days":no_of_days[i]})
        print(stageList)
        print(type(dept_ID))
        if len(dept_ID)==1:
            applications.insert_one({"appname":appname,"appid":appID,"stageList":stageList,"lastDept":dept_ID[0],"timeCreated":datetime.now()})
        else:
            applications.insert_one(
                {"appname": appname, "appid": appID, "stageList": stageList, "lastDept": dept_ID[len(dept_ID)-1],
                 "timeCreated": datetime.now()})
        return "1"
    else:
        return "GET method not allowed"

    
    
@backendapp.route("/get_app_types",methods=["GET","POST"])
def get_app_types():
    '''
    if request.method == "POST":
        if "application/x-www-form-urlencoded" in request.headers["Content-Type"]:
            postData = request.form
        else:
            postData = request.get_json()
    '''
    appids = list(applications.find({}, {'appid': 1,"appname":1,"stageList":1,"timeCreated":1 ,'_id': 0}))
    print(appids)
    '''
    pappids = []
    for i in appids:
        pappids.append(i['appid'])
    print(pappids)
    '''
    response = {"appids":appids}
    return jsonify(response)




@backendapp.route("/add_dept",methods=["GET","POST"])
def add_dept():
    print(request.headers)
    if request.method == "POST":
        if "application/x-www-form-urlencoded" in request.headers["Content-Type"]:
            postData = request.form
        else:
            postData = request.get_json()
    dept_id = postData["dept_id"]
    dept_name = postData["dept_name"]
    print(postData)
    print(dept_id)
    result = dept.find_one({"dept_id":dept_id})
    if result != None:
        response = {"status":"2"}
    else:
        result = dept.insert_one({"dept_id":dept_id,"dept_name":dept_name,"timeCreated":datetime.now(),"count":0,"delayedCount":0,"completedCount":0,"currFiles":[],"delayedFiles":[],"prevFiles":[]})
        if result !=None:
            response = {"status":"1"}
        else:
            response  = {"status":"0"}
    return  jsonify(response)



@backendapp.route("/get_dept_ids",methods=["GET","POST"])
def get_dept_ids():
    '''
    if request.method == "POST":
        if "application/x-www-form-urlencoded" in request.headers["Content-Type"]:
            postData = request.form
        else:
            postData = request.get_json()
    '''
    dept_ids = list(dept.find({}, {'dept_id': True,"dept_name":True,"timeCreated":True,'_id': False}))
    print(dept_ids)
    '''
    pdept_ids = []
    for i in dept_ids:
        pdept_ids.append(i['appid'])
    print(pdept_ids)
    '''
    response = {"dept_ids":dept_ids}
    return jsonify(response)

#ADD HOLIDAY IN COUNTING



def date_by_adding_business_days(from_date, add_days):
    business_days_to_add = add_days
    current_date = from_date
    l = list(holidays.find({}, {"dateDay": True, "_id": False}))
    hh = [datetime.strptime(d['dateDay'], "%Y-%m-%d").date() for d in l]
    #print(hh)
    while business_days_to_add > 0:
        current_date += timedelta(days=1)
        weekday = current_date.weekday()
        if current_date.date() in hh:
            #print("In HH")
            continue
        if weekday >= 5:  # sunday = 6
            continue
        business_days_to_add -= 1
    return current_date



def least_file_emp(dept_id):
    results = emp_stats.find({"dept_id":dept_id},{"email_id":True,"count":True,"_id":False})
    resultsDict = {}
    for i in results:
        resultsDict[i["email_id"]]=i["count"]
    Dic = {k: v for k, v in sorted(resultsDict.items(), key=lambda item: item[1])}
    return list(Dic)[0]



'''                 Codes Generation Barcode QRcode             '''
@backendapp.route("/generate_barcode", methods=["GET", "POST"])
def generate_barcode():
    if request.method == "GET":
        appid = request.args.get('q')
        print("APP ID : " + appid)
        d = datetime.now()
        t = d.timestamp()
        bcode_string = appid + str(t).split('.')[0]
        bcode = generate(name="code128", code=bcode_string, writer=ImageWriter(),
                         output="bcodes/{}".format(bcode_string))
        if bcode == None:
            response = {"status": 0, "message": "Barcode_Generation_Failed"}
            return jsonify(response)
        bcode_image = open("bcodes/{}.png".format(bcode_string), 'rb')
        if bcode_image == None:
            response = {"status": 0, "message": "Barcode_Image_Failed_To_LOAD"}
            return jsonify(response)

        app_stagelist = applications.find_one({"appid": appid})["stageList"]

        firstDept= app_stagelist[0]["dept_id"]
        lastDept = app_stagelist[len(app_stagelist) - 1]["dept_id"]

        file_expected = {}
        total = 0
        for i in app_stagelist:
            file_expected[i["dept_id"]] = date_by_adding_business_days(d, total + int(i["no_of_days"]))
            total += int(i["no_of_days"])

        try:
            emp = least_file_emp(firstDept)
            result = files.insert_one({"fid": bcode_string, "applicationType": appid, "timeCreated": d, \
                                       "fileDone": False, "currDept": firstDept, "currEmp": emp,"prevDept":None,"prevEmp":None,"scanned":False, "delayed": False, \
                                       "delayedDays": 0, "expectedTimeline": file_expected,
                                       "expectedTimelineDuplicate": file_expected, \
                                       "stageList": [],"firstDept":firstDept,"lastDept":lastDept, "delayNotificationSent": None, "lastScanTime": "Not Scanned yet."})

            emp_stats_result = emp_stats.find_one({"email_id":emp},{"incomingFiles":True,"_id":False})
            emp_incoming_files=emp_stats_result["incomingFiles"]
            emp_incoming_files[bcode_string]={"time":d,"from":"Barcode Generation Dept","remark":"","alert":False}

            emp_result = emp_stats.find_one_and_update({"email_id":emp},{"$set":{"incomingFiles":emp_incoming_files},"$inc":{"count":1}})

            data = base64.b64encode(bcode_image.read()).decode("utf-8")
            response = {"status": "1", "message": "Success","code_string":bcode_string ,"image": data}
            print("response")
            return jsonify(response)
        except:
            response = {"status": "0", "message": "DB insert Failed"}
            raise
            return jsonify(response)
    else:
        return "POST method not allowed"

@backendapp.route("/generate_qrcode", methods=["GET","POST"])
def generate_qrcode():
    if request.method == "GET":
        appid = request.args.get('q')
        print("APP ID : " + appid)
        d = datetime.now()
        t = d.timestamp()
        bcode_string = appid + str(t).split('.')[0]
        qr_code = qrcode.make('bcode_string', image_factory=PymagingImage)
        try:
            with open("bcodes/{}.png".format(bcode_string), "wb") as f:
                qr_code.save(f)
        except:
            response = {"status": 0, "message": "QRCode_ImageSave_Failed"}
            return jsonify(response)
        if qr_code == None:
            response = {"status": 0, "message": "Barcode_Generation_Failed"}
            return jsonify(response)
        bcode_image = open("bcodes/{}.png".format(bcode_string), 'rb')
        if bcode_image == None:
            response = {"status": 0, "message": "Barcode_Image_Failed_To_LOAD"}
            return jsonify(response)

        app_stagelist = applications.find_one({"appid": appid})["stageList"]

        firstDept= app_stagelist[0]["dept_id"]
        lastDept = app_stagelist[len(app_stagelist) - 1]["dept_id"]

        file_expected = {}
        total = 0
        for i in app_stagelist:
            file_expected[i["dept_id"]] = date_by_adding_business_days(d, total + int(i["no_of_days"]))
            total += int(i["no_of_days"])

        try:
            emp = least_file_emp(firstDept)
            result = files.insert_one({"fid": bcode_string, "applicationType": appid, "timeCreated": d, \
                                       "fileDone": False, "currDept": firstDept, "currEmp": emp,"prevDept":None,"prevEmp":None,"scanned":False, "delayed": False, \
                                       "delayedDays": 0, "expectedTimeline": file_expected,
                                       "expectedTimelineDuplicate": file_expected, \
                                       "stageList": [],"firstDept":firstDept,"lastDept":lastDept, "delayNotificationSent": None, "lastScanTime": "Not Scanned yet."})

            emp_stats_result = emp_stats.find_one({"email_id":emp},{"incomingFiles":True,"_id":False})
            emp_incoming_files=emp_stats_result["incomingFiles"]
            emp_incoming_files[bcode_string]={"time":d,"from":"Barcode Generation Dept","remark":"","alert":False}

            emp_result = emp_stats.find_one_and_update({"email_id":emp},{"$set":{"incomingFiles":emp_incoming_files},"$inc":{"count":1}})

            data = base64.b64encode(bcode_image.read()).decode("utf-8")
            response = {"status": "1", "message": "Success","code_string":bcode_string, "image": data}
            print("response")
            return jsonify(response)
        except:
            response = {"status": "0", "message": "DB insert Failed"}
            raise
            return jsonify(response)
    else:
        return "POST method not allowed"
'''                 Codes Generation Barcode QRcode             '''

@backendapp.route("/chk_email", methods=["GET"])
def chk_email():
    email = request.args.get('q')
    print(email)
    result = emp_data.find_one({"email_id": email})
    if result == None:
        return "1"
    else:
        return "0"

    
    
@backendapp.route("/chk_appid", methods=["GET"])
def chk_appid():
    appid = request.args.get('q')
    print(appid)
    result = applications.find_one({"appid": appid})
    if result == None:
        return "1"
    else:
        return "0"

    
    
@backendapp.route("/emp_create",methods=["GET","POST"])
def emp_create():
    if request.method == "POST":
        if "application/x-www-form-urlencoded" in request.headers["Content-Type"]:
            postData = request.form
        else:
            postData = request.get_json()
        email = postData["email"]
        password = postData["pword"]
        fname = postData["fname"]
        lname = postData["lname"]
        mno = postData["mno"]
        dept_id = postData["dept_id"]
        result1=emp_data.insert_one({"email_id":email,"password":password,"fname":fname,"lname":lname,"mno":mno,"dept_id":dept_id,"date_created":datetime.now()})
        result2=emp_stats.insert_one({"email_id":email,"mno":mno,"dept_id":dept_id,"count":0,"incomingFiles":{},"outgoingFiles":{},"currFiles":[],"prevFiles":[]})
        if result1!=None and result2 !=None:
            return "1"
        else:
            return "0"
    else:
        return "GET method is not allowed"

    
    
@backendapp.route("/emp_login",methods=["POST","GET"])
def emp_login():
    if request.method == "POST":
        postData = request.get_json()
        print(postData)
        email = postData["email"]
        password = postData["pass"]

        results = emp_data.find_one({"email_id":email,"password":password})
        if results != None:
            #Login successful
            #details = {"fname":results["fname"],"lname":results["lname"],"email":results["email_id"]}
            details = {"fname": results["fname"], "lname": results["lname"], "email": results["email_id"],"dept_id":results["dept_id"]}
            response = {"status": 1, "message": details}
            print(jsonify(response))
            return jsonify(response)
        else:
            #Login Failed
            response = {"status": 0, "message": "Wrong details"}
            return jsonify(response)

    else:
        #Illegal connection attempt
        response = {"status": 2, "message": "Method error"}
        return jsonify(response)

    
    
@backendapp.route("/bcode_entry",methods=["GET","POST","OPTIONS"]) #TEST for PC
def bcode_entry():
    if request.method == "POST":
        #print(request.headers["Content-Type"])
        if "application/x-www-form-urlencoded" in request.headers["Content-Type"]:
            postData = request.form
        else:
            postData = request.get_json()
        print("PostData : "+str(postData))
        bcode = postData["bcodeTxt"]
        #print(bcode)
        dept_id = postData["deptID"]
        email_id = postData["email"] #Jo scan kar raha hai; Iske incoming se file nikalna hai
        #print(email_id)
        d=datetime.now()
        file_query_result = files.find_one({"fid": bcode})

        prevEmp = file_query_result["prevEmp"] #Iske outgoing se file nikalna hai
        lst =  file_query_result["stageList"]
        emp_stats_query_result = emp_stats.find_one({"email_id":email_id})
        currFiles = emp_stats_query_result["currFiles"]

        dept_stats_query_result = emp_stats.find_one({"dept_id":dept_id})
        currFilesDept = dept_stats_query_result["currFiles"]

        lst.append({"deptID":dept_id, "empID": email_id, "timeArrived": d,"remark":"","delay":0})
        try:
            files.find_one_and_update({"fid": bcode}, {"$set": {"stageList": lst,"currDept":dept_id,"currEmp":email_id,"lastScanTime":d,"scanned":True}})
            currFiles.append({"fid":bcode,"timeArrived":d})
            currFilesDept.append({"fid":bcode,"timeArrived":d,"emp_id":email_id})
            #Removing from incoming of emp scanning
            emp_incoming_files_query = emp_stats.find_one({"email_id":email_id},{"incomingFiles":True,"_id":False})
            emp_incoming_files = emp_incoming_files_query["incomingFiles"]
            emp_incoming_files.pop(bcode)
            emp_stats.find_one_and_update({"email_id":email_id},{"$set":{"currFiles":currFiles,"incomingFiles":emp_incoming_files}})
            # Removing from incoming of emp scanning
            # Removing from outgoing of prev emp
            print("EMAIL_ID : {}".format(prevEmp))
            if prevEmp != None:
                emp_outgoing_files_query = emp_stats.find_one({"email_id": prevEmp}, {"outgoingFiles": True, "_id": False})
                emp_outgoing_files = emp_outgoing_files_query["outgoingFiles"]
                emp_outgoing_files.pop(bcode)
                emp_stats.find_one_and_update({"email_id":prevEmp},{"$set":{"outgoingFiles":emp_outgoing_files}})
            # Removing from outgoing of prev emp
            dept.find_one_and_update({"dept_id":dept_id},{"$set":{"currFiles":currFilesDept},"$inc":{"count":1}})
            result = True
        except:
            result = None
            raise

        #bcode_insert_query = "Select fname,lname,email_id from emp_data where email_id = '{0}' and password = '{1}' LIMIT 1;".format(email,password)

        if result != None:
            #Update successful
            response = {"status": "1", "message": "Update Done"}
            print(response)
            return jsonify(response)
        else:
            #Login Failed
            response = {"status": 0, "message": "Update failed"}
            return jsonify(response)

    else:
        #Illegal connection attempt
        response = {"status": 2, "message": "Method error"}
        return jsonify(response)

    
    
def chk_delayed(file):
    today = datetime.now().date()
    result = files.find_one({"fid":file})
    currDept = result["currDept"]
    expectedTimeline = result["expectedTimelineDuplicate"]
    expectedDate = expectedTimeline[currDept].date()
    print("{} + {}".format(expectedDate,today))
    if(expectedDate<today):
        return [int((today-expectedDate).days),currDept,result["lastDept"]]
    else:
        return [None,currDept,result["lastDept"]]


    
'''                                                  Notifications                                                '''

@backendapp.route("/get_emp_notifications",methods=["GET","POST"])
def get_emp_notifications():
    if request.method == "POST":
        if "application/x-www-form-urlencoded" in request.headers["Content-Type"]:
            postData = request.form
        else:
            postData = request.get_json()
        email = postData['email_id']
        #print("Email : {}".format(email))
        chk_new_notification = notifications.find_one({"email_id":email,"read":False})
        if chk_new_notification != None:
            #New notifications
            print("New Notifications there.")

            notifisReadFalseCount=notifications.find({"email_id":email,"read":False},{"notificationID":True}).count()
            #notifisReadFalseList=list(notifisReadFalse)
            notifis = notifications.find({"email_id":email},{"notificationID":True,"timeCreated":True,"message":True,"read":True,"_id":0}).sort("timeCreated",pymongo.DESCENDING)

            notifisList = list(notifis)

            #print("NOTIFIS : {}".format(list(notifis)))
            response = {"status":"1","new_notification":"1","count":notifisReadFalseCount,"notifis":notifisList}
        else:
            #No new notifications
            print("No New Notifications there.")
            notifis = notifications.find({"email_id": email}, {"notificationID":True,"timeCreated": True, "message": True,"read":True,"_id":0}).sort(
                "timeCreated", pymongo.DESCENDING)
            #print("NOTIFIS : ".format(list(notifis)))
            notifisList = list(notifis)
            response = {"status": "1", "new_notification": "0","count":0, "notifis": notifisList}
        print("Notifications : {}".format(response))
        return jsonify(response)
    else:
        return "POST method not allowed"

    
    
@backendapp.route("/update_all_notifications_status",methods=["GET","POST"])
def update_all_notifications_status():
    if request.method == "POST":
        if "application/x-www-form-urlencoded" in request.headers["Content-Type"]:
            postData = request.form
        else:
            postData = request.get_json()
        email = postData['email_id']
        notifications.update_many({"email_id":email,"read":False},{"$set":{"read":True}})
        response={"status":"1"}
        return jsonify(response)
    else:
        return "POST method not allowed"

    
    
@backendapp.route("/update_notification_status",methods=["GET","POST"]) #Not Complete
def update_notification_status():
    if request.method == "GET":
        notificationID = request.args.get('notificationID')
        result= notifications.find_one_and_update({"notificationID": notificationID}, {"$set": {"read": True}})
        print("RESULT : {}".format(result))
        response = {"status": "1"}
        return jsonify(response)
    else:
        return "POST method not allowed"


    
    
@backendapp.route("/file_not_arrived_complain",methods=["GET","POST"])
def file_not_arrived_complain():
    if request.method=="POST":
        if "application/x-www-form-urlencoded" in request.headers["Content-Type"]:
            postData = request.form
        else:
            postData = request.get_json()
        print("PostData : {}".format(postData))
        notificationID = postData['notificationid']
        email = postData['email']
        file = postData['file']
        fromEmail = postData['from']
        try:
            chkapp = postData['app']
            time = postData['time']
        except:
            time = datetime.utcfromtimestamp(int(postData['time']))

        print("notificationID : {}".format(notificationID))
        print("email : {}".format(email))
        print("fromEmail : {}".format(fromEmail))
        print("time : {}".format(fromEmail))
        message= file_complain_message.format(email,file,fromEmail,time)
        print(message)
        try:
            adminInbox.insert_one({"notificationID":notificationID,"emp_id":email,"message":message,"timeCreated":datetime.now(),"read":False,"timeAttended":None})
            incomingFiles = emp_stats.find_one({"email_id":email},{"incomingFiles":1,"_id":0})
            print(incomingFiles)
            incomingFiles['incomingFiles'][file]["alert"] = True
            emp_stats.find_one_and_update({"email_id":email},{"$set":{"incomingFiles":incomingFiles['incomingFiles']}})
            response = {"status":"1"}
        except:
            response = {"status":"0"}
            raise
        print(response)
        return jsonify(response)
    else:
        return "GET not allowed!"

    
    
@backendapp.route("/get_file_complaints",methods=["GET","POST"])
def get_file_complaints():
    if request.method =="GET":
        attended = adminInbox.find({"read":True},{"_id":0})
        attendedList = list(attended)
        notattended = adminInbox.find({"read": False},{"_id":0})
        notattendedList = list(notattended)
        details = {"attended":attendedList,"notattended":notattendedList}
        response = {"status":"1","details":details}
        print(response)
        return jsonify(response)
    else:
        return "POST not allowed"

    
    
@backendapp.route("/update_file_complaint_notification",methods=["GET","POST"])
def update_file_complaint_notification():
    if request.method =="POST":
        if "application/x-www-form-urlencoded" in request.headers["Content-Type"]:
            postData = request.form
        else:
            postData = request.get_json()
        notificationID = postData['notificationid']
        adminInbox.find_one_and_update({"notificationID":notificationID},{"$set":{"read":True,"timeAttended":datetime.now()}})
        response = {"status":"1"}
        return jsonify(response)
    else:
        return "GET not allowed"
    
'''                                                  Notifications                                               '''

'''                                                        Forward                                               '''

@backendapp.route("/forward",methods=["GET","POST"]) #TEST
def forward():
    if request.method == "GET" or request.method=="POST":
        if request.method == "GET":
            fid = request.args.get('filename')
            remark = request.args.get('remark')
        else:
            postData = request.get_json()
            print("POSTDATA : {}".format(postData))
            fid = postData["filename"]
            remark = postData["remark"]
        #print("fid : {}".format(fid))
        d = datetime.now()
        result = files.find_one({"fid": fid})
        dept_id = result["currDept"]
        fileStageList = result["stageList"]
        #print("Filestage : {} ".format(fileStageList))
        applicationType = result["applicationType"]
        applications_query_result = applications.find_one({"appid":applicationType})
        appStageList = applications_query_result["stageList"]
        expectedTimelineDuplicate = result["expectedTimelineDuplicate"]
        currDept = result["currDept"]
        email_id = result["currEmp"]
        #print("email id :  {}".format(email_id))

        emp_stats_query_result=emp_stats.find_one({"email_id":email_id})
        dept_stats_query_result = dept.find_one({"dept_id": dept_id})

        currFiles = emp_stats_query_result["currFiles"]
        prevFiles = emp_stats_query_result["prevFiles"]
        currFilesDept = dept_stats_query_result["currFiles"]
        prevFilesDept = dept_stats_query_result["prevFiles"]

        delay = chk_delayed(fid)
        #print("Currfiles : {}".format(currFiles))
        #print("Length of currfiles : {}".format(len(currFiles)))
        for i in range(len(currFiles)):
            if currFiles[i]['fid']==fid:
                index_in_curr_file = i
        for i in range(len(currFiles)):
            if currFilesDept[i]['fid']==fid:
                index_in_curr_file_dept = i
        if(delay[0]!=None):
            for i in expectedTimelineDuplicate.keys():
                if i != currDept:
                    expectedTimelineDuplicate[i]=date_by_adding_business_days(expectedTimelineDuplicate[i],delay[0])
        else:
            delay[0] = 0
        next_ = False
        nextDept = None
        for i in appStageList:
            #print(i["dept_id"]+" "+currDept)
            if next_ ==False:
                if i["dept_id"]==currDept:
                    fileStageList[len(fileStageList)-1]["remark"]=remark

                    fileStageList[len(fileStageList) - 1]["delay"] = delay[0] #CheckThis
                    #print("filestageList update :")
                    #print("\t {}".format(str(fileStageList)))
                    next_ = True
            else:
                #print("Next found")
                nextDept = i["dept_id"]
                break
        if nextDept == None:
            #FileDone
            fileDone = True
            files.find_one_and_update({"fid": fid},{
                "$set": {"expectedTimelineDuplicate": expectedTimelineDuplicate,"stageList":fileStageList,
                         "currDept": None,"currEmp":None,"prevDept":currDept,"prevEmp":email_id,
                         "delayed":False,"delayedDays":0,"fileDone": fileDone,"scanned":False}})


            prevFiles.append({"fid": fid, "delay": delay[0],"timeArrived":currFiles[index_in_curr_file]["timeArrived"],
                              "timeCompleted":d})
            prevFilesDept.append({"fid": fid,"emp_id":email_id,"delay": delay[0],"timeArrived":currFiles[index_in_curr_file]["timeArrived"],
                              "timeCompleted":d})
            #currFiles.remove(fid)
            currFiles.pop(index_in_curr_file)
            currFilesDept.pop(index_in_curr_file_dept)

            emp_stats.find_one_and_update({"email_id":email_id},
                                          {"$set":{"currFiles":currFiles,"prevFiles":prevFiles},"$inc":{"count":-1}})
            dept.find_one_and_update({"dept_id": dept_id}, {"$inc": {"count": -1,"completedCount":1}, "$set":{"currFiles":currFilesDept,"prevFiles":prevFilesDept}})

            r = {"status": "1"}
            
            return jsonify(r)
        else:
            #FileNotDone
            #UpdateCurrdept
            emp = least_file_emp(nextDept)
            files.find_one_and_update({"fid": fid}, {
                "$set": {"expectedTimelineDuplicate": expectedTimelineDuplicate,"stageList":fileStageList,
                         "currDept": nextDept,"currEmp":emp,"prevDept":currDept,"prevEmp":email_id,
                         "delayed":False,"delayedDays":0,"scanned":False}})

            prevFiles.append({"fid": fid, "delay": delay[0], "timeArrived": currFiles[index_in_curr_file]["timeArrived"],
                              "timeCompleted": d})
            prevFilesDept.append({"fid": fid, "emp_id": email_id, "delay": delay[0],
                                  "timeArrived": currFiles[index_in_curr_file]["timeArrived"],
                                  "timeCompleted": d})
            # currFiles.remove(fid)
            currFiles.pop(index_in_curr_file)
            currFilesDept.pop(index_in_curr_file_dept)

            #email_id ke outcoming mein entry
            emp_outgoing_result = emp_stats.find_one({"email_id":email_id},{"outgoingFiles":True,"_id":False})
            emp_outgoing_files = emp_outgoing_result["outgoingFiles"]
            emp_outgoing_files[fid]={"time":d,"to":emp,"remark":remark}

            emp_stats.find_one_and_update({"email_id": email_id},
                                          {"$set": {"currFiles": currFiles, "prevFiles": prevFiles,"outgoingFiles": emp_outgoing_files},"$inc":{"count":-1}})
            # email_id ke outcoming mein entry
            # emp ke incoming mein entry
            emp_incoming_result = emp_stats.find_one({"email_id":emp},{"incomingFiles":True,"_id":False})
            emp_incoming_files = emp_incoming_result["incomingFiles"]
            emp_incoming_files[fid]={"time":d,"from":email_id,"remark":remark,"alert":False}
            emp_stats.find_one_and_update({"email_id":emp},{"$set":{"incomingFiles":emp_incoming_files},"$inc":{"count":1}})
            # emp ke incoming mein entry
            dept.find_one_and_update({"dept_id": dept_id}, {"$inc": {"count": -1, "completedCount": 1},
                                                            "$set": {"currFiles": currFilesDept,
                                                                     "prevFiles": prevFilesDept}})

            dept.find_one_and_update({"dept_id": nextDept}, {"$inc": {"count": 1}})

            r = {"status": "1"}
            return jsonify(r)
    else:
        return "POST not allowed"
'''                                                        Forward                                               '''

'''                                                        Forward                                               '''


@backendapp.route("/same_dept_forward", methods=["GET", "POST"])  # TEST
def same_dept_forward():
    if request.method == "GET" or request.method == "POST":
        if request.method == "GET":
            fid = request.args.get('filename')
            remark = request.args.get('remark')
            nextEmp = request.args.get('nextEmp')
        else:
            postData = request.get_json()
            print("POSTDATA : {}".format(postData))
            fid = postData["filename"]
            remark = postData["remark"]
            nextEmp = postData["nextEmp"]
        # print("fid : {}".format(fid))
        print("-----"+ nextEmp)
        d = datetime.now()
        result = files.find_one({"fid": fid})
        #dept_id = result["currDept"]
        fileStageList = result["stageList"]
        #print("Filestage : {} ".format(fileStageList))
        #applicationType = result["applicationType"]
        #applications_query_result = applications.find_one({"appid": applicationType})
        #appStageList = applications_query_result["stageList"]
        #expectedTimelineDuplicate = result["expectedTimelineDuplicate"]
        currDept = result["currDept"]
        email_id = result["currEmp"]
        # print("email id :  {}".format(email_id))

        emp_stats_query_result = emp_stats.find_one({"email_id": email_id})
        #dept_stats_query_result = dept.find_one({"dept_id": dept_id})

        currFiles = emp_stats_query_result["currFiles"]
        prevFiles = emp_stats_query_result["prevFiles"]
        #currFilesDept = dept_stats_query_result["currFiles"]
        #prevFilesDept = dept_stats_query_result["prevFiles"]


        delay = chk_delayed(fid)
        delayed = True
        if (delay[0] == None):
            delay[0] = 0
            delayed = False
        #print("Currfiles : {}".format(currFiles))
        #print("Length of currfiles : {}".format(len(currFiles)))
        for i in range(len(currFiles)):
            if currFiles[i]['fid'] == fid:
                index_in_curr_file = i



        #nextDept = None
        '''                 DING DING           '''
        fileStageList[len(fileStageList) - 1]["remark"] = remark

        fileStageList[len(fileStageList) - 1]["delay"] = delay[0]  # CheckThis

        files.find_one_and_update({"fid": fid}, {
            "$set": {"stageList": fileStageList,
                     "currEmp": nextEmp, "prevDept": currDept, "prevEmp": email_id,
                     "delayed": delayed, "delayedDays": delay[0], "scanned": False}})

        prevFiles.append(
            {"fid": fid, "delay": delay[0], "timeArrived": currFiles[index_in_curr_file]["timeArrived"],
             "timeCompleted": d})

        # currFiles.remove(fid)
        currFiles.pop(index_in_curr_file)

        # email_id ke outcoming mein entry
        emp_outgoing_result = emp_stats.find_one({"email_id": email_id}, {"outgoingFiles": True, "_id": False})
        emp_outgoing_files = emp_outgoing_result["outgoingFiles"]
        emp_outgoing_files[fid] = {"time": d, "to": nextEmp, "remark": remark}

        emp_stats.find_one_and_update({"email_id": email_id},
                                      {"$set": {"currFiles": currFiles, "prevFiles": prevFiles,
                                                "outgoingFiles": emp_outgoing_files}, "$inc": {"count": -1}})
        # email_id ke outcoming mein entry

        # emp ke incoming mein entry
        emp_incoming_result = emp_stats.find_one({"email_id": nextEmp}, {"incomingFiles": True, "_id": False})
        emp_incoming_files = emp_incoming_result["incomingFiles"]
        emp_incoming_files[fid] = {"time": d, "from": email_id, "remark": remark, "alert": False}
        emp_stats.find_one_and_update({"email_id": nextEmp},
                                      {"$set": {"incomingFiles": emp_incoming_files}, "$inc": {"count": 1}})
        # emp ke incoming mein entry


        r = {"status": "1"}
        return jsonify(r)
        '''                 DING DING                  '''



    else:
        return "POST not allowed"


'''                                                        Forward                                               '''


'''                                                       ALL STATS                                             '''
'''                                                       FileTrack                                             '''

@backendapp.route("/get_file_path",methods=["GET","POST"])#TEST
def get_file_path():
    if request.method == "GET":
        fid = request.args.get('q')
        print(fid)
        result = files.find_one({"fid": fid})
        fileDone = result["fileDone"]
        lastScanTime = result["lastScanTime"]
        lst = result["stageList"]
        if fileDone==True:
            totalDelayed = 0
            for i in lst:
                totalDelayed += i["delay"]
            response = {"fileDone": fileDone,"delayedBy":totalDelayed,"list":lst}
        else:
            applicationType = result["applicationType"]
            currDept = result["currDept"]
            currEmp = result["currEmp"]
            delay = chk_delayed(fid)
            print("appType : {} + currDept : {}".format(applicationType,currDept))
            '''
            estimate_days = estimateTime.find_one({"appid":applicationType,"dept_id":currDept},{"estimateDays":True,"_id":False})
            print(list(estimate_days))
            estimate_date = date_by_adding_business_days(datetime.now(),estimate_days["estimateDays"])
            '''


            lst = result["stageList"]

            scanned = result["scanned"]

            if delay[0] !=None:
                estimate_date = date_by_adding_business_days(datetime.now(),
                                                             mlModel.predict([[deptToNumber[currDept], delay[0],
                                                                               appToNumber[applicationType]]])[0])

                response = {"status":"1","delay":"1","delayedBy":delay[0],"currDept":currDept,"currEmp":currEmp,"estimate_date":estimate_date,"lastScanTime":lastScanTime,"list":lst,"scanned":scanned,"fileDone":fileDone}
            else:
                estimate_date = date_by_adding_business_days(datetime.now(),
                                                             mlModel.predict([[deptToNumber[currDept], 0,
                                                                               appToNumber[applicationType]]])[0])

                response = {"status":"1","delay":"0","delayedBy":0,"currDept":currDept,"currEmp":currEmp,"estimate_date":estimate_date,"lastScanTime":lastScanTime,"list":lst,"scanned":scanned,"fileDone":fileDone}
        print(response)
        return jsonify(response)
    else:
        return "POST method not allowed"
'''                                                       FileTrack                                             '''

@backendapp.route("/get_dashboard_stats",methods=["GET","POST"])
def get_dashboard_stats():
    if request.method == "GET":
        total_count = files.find({},{"fid":True,"_id":False}).count()
        completed_count =  files.find({"fileDone":True},{"fid":True,"_id":False}).count()
        delayed_count = files.find({"delayed":True},{"fid":True,"_id":False}).count()
        details = {"total_count":total_count,"completed_count":completed_count,"delayed_count":delayed_count}
        response = {"status":"1","details":details}
        return jsonify(response)
    else:
        return "POST method not allowed"

    
    
@backendapp.route("/get_all_files",methods=["GET","POST"])
def get_all_files():
    if request.method == "GET":
        all_files = files.find({},{"_id":False})
        details = {"all_files":list(all_files)}
        response = {"status":"1","details":details}
        return jsonify(response)
    else:
        return "POST method not allowed"

    
    
@backendapp.route("/get_completed_files",methods=["GET","POST"])
def get_completed_files():
    if request.method == "GET":
        completed_files = files.find({"fileDone":True},{"_id":False})
        details = {"completed_files":list(completed_files)}
        response = {"status":"1","details":details}
        return jsonify(response)
    else:
        return "POST method not allowed"

    
    
@backendapp.route("/get_processing_files",methods=["GET","POST"])
def get_processing_files():
    if request.method == "GET":
        processing_files = files.find({"fileDone":{"$ne" : True},"delayed":{"$ne" : True}},{"_id":False})
        details = {"processing_files":list(processing_files)}
        response = {"status":"1","details":details}
        return jsonify(response)
    else:
        return "POST method not allowed"

    
    
@backendapp.route("/get_delayed_files",methods=["GET","POST"])
def get_delayed_files():
    if request.method == "GET":
        delayed_files = files.find({"delayed":True},{"_id":False})
        details = {"delayed_files":list(delayed_files)}
        response = {"status":"1","details":details}
        return jsonify(response)
    else:
        return "POST method not allowed"

    
    
def chk_delayed_dept(file):
    today = datetime.now().date()
    print("FID : {}".format(file))
    result = files.find_one({"fid":file})
    currDept = result["currDept"]
    expectedTimeline = result["expectedTimelineDuplicate"]
    expectedDate = expectedTimeline[currDept].date()
    print("{} + {}".format(expectedDate,today))
    if(expectedDate<today):
        return [int((today-expectedDate).days),result["currEmp"]]
    else:
        return [None,result["currEmp"]]

    
@backendapp.route("/get_dept_stats",methods=["GET","POST"])
def get_dept_stats():
    if request.method == "GET":
        dept_id = request.args.get('dept_id')
        result = dept.find_one({"dept_id":dept_id})
        prevFiles=result["prevFiles"]
        delayedCount = 0
        for i in prevFiles:
            if i["delay"] != 0:
                delayedCount += 1
        details= {"totalCount":result["completedCount"],"delayedCount":delayedCount}
        response = {"status":"1","message":details}
        return jsonify(response)
    else:
        return ("Post method not allowed")

    
    
@backendapp.route("/get_dept_stats_current_month",methods=["GET","POST"])
def get_dept_stats_current_month():
    if request.method=="GET":
        d=datetime.now()
        dept_id = request.args.get('dept_id')
        result = dept.find_one({"dept_id": dept_id})
        prevFiles = result["prevFiles"]
        prevFilesFid = []
        prevFilesFidDelayDict={}
        for i in prevFiles:
            prevFilesFid.append(i["fid"])
            prevFilesFidDelayDict[i["fid"]]=i["delay"]

        thisMonthDays=calendar.monthrange(d.year, d.month)[1]

        d1 = datetime(year=d.year, month=d.month, day=1, hour=0, minute=0, second=0, microsecond=0)
        d2 = datetime(year=d.year, month=d.month, day=thisMonthDays, hour=23, minute=59, second=59, microsecond=999999)
        result = files.find({"fid":{"$in":prevFilesFid},"timeCreated":{"$gte":d1,"$lte":d2}},{"fid":True,"timeCreated":True,"_id":True})
        resultList = list(result)
        delayedCount = 0
        thisMonthPrevFiles = [i["fid"] for i in resultList]
        for i in thisMonthPrevFiles:
            if prevFilesFidDelayDict[i] != 0:
                delayedCount += 1

        details = {"totalCount":result.count(),"delayedCount":delayedCount}
        response = {"status":"1","details":details}
        return jsonify(response)
    else:
        return "POST not allowed"

    
    
@backendapp.route("/get_dept_stats_quarter",methods=["GET","POST"])
def get_dept_stats_quarter():
    if request.method=="GET":
        d=datetime.now()
        dept_id = request.args.get('dept_id')
        quarter = request.args.get('quarter')
        print("QUARTER TYPE : {}".format(type(quarter)))
        startMonth = quarterDetails[quarter][0]
        endMonth = quarterDetails[quarter][1]
        result = dept.find_one({"dept_id": dept_id})
        prevFiles = result["prevFiles"]
        prevFilesFid = []
        prevFilesFidDelayDict = {}
        for i in prevFiles:
            prevFilesFid.append(i["fid"])
            prevFilesFidDelayDict[i["fid"]] = i["delay"]
        print("PrevFilesFidDelayDict : {}".format(prevFilesFidDelayDict))
        startMonthDays=calendar.monthrange(d.year, startMonth)[1]
        endMonthDays=calendar.monthrange(d.year,endMonth)[1]

        print("PrevFilesFid : {}".format(prevFilesFid))
        d1 = datetime(year=d.year, month=startMonth, day=1, hour=0, minute=0, second=0, microsecond=0)
        d2 = datetime(year=d.year, month=endMonth, day=endMonthDays, hour=23, minute=59, second=59, microsecond=999999)
        print("D1 : {}".format(d1))
        print("D2 : {}".format(d2))
        '''
        result = files.find({"timeCreated": {"$gte": d1, "$lte": d2}},
                            {"fid": True, "timeCreated": True, "_id": True})
        resultList = list(result)
        print("ResultList  : {}".format(resultList))
        '''
        result = files.find({"fid":{"$in":prevFilesFid},"timeCreated":{"$gte":d1,"$lte":d2}},{"fid":True,"timeCreated":True,"_id":True})
        resultList = list(result)
        #print("ResultList  : {}".format(resultList))
        delayedCount = 0
        thisQuarterPrevFiles = [i["fid"] for i in resultList]
        print("thisQuarterPrevFiles  : {}".format(thisQuarterPrevFiles))
        for i in thisQuarterPrevFiles:
            if prevFilesFidDelayDict[i] != 0:
                delayedCount += 1
        details = {"totalCount":len(resultList),"delayedCount":delayedCount}
        response = {"status":"1","details":details}
        print(response)
        return jsonify(response)
    else:
        return "POST not allowed"

    
    
@backendapp.route("/get_dept_stats_year",methods=["GET","POST"])
def get_dept_stats_year():
    if request.method == "GET":
        d = datetime.now()
        dept_id = request.args.get('dept_id')
        year = int(request.args.get('year'))

        result = dept.find_one({"dept_id": dept_id})
        prevFiles = result["prevFiles"]

        prevFilesFid = []
        prevFilesFidDelayDict = {}
        for i in prevFiles:
            prevFilesFid.append(i["fid"])
            prevFilesFidDelayDict[i["fid"]] = i["delay"]

        d1 = datetime(year=year, month=1, day=1, hour=0, minute=0, second=0,
                               microsecond=0)
        d2 = datetime(year=year, month=12, day=31, hour=23, minute=59, second=59,
                               microsecond=999999)
        result = files.find({"fid": {"$in": prevFilesFid}, "timeCreated": {"$gte": d1, "$lte": d2}},
                            {"fid": True, "timeCreated": True, "_id": True})
        resultList=list(result)
        delayedCount = 0
        thisYearPrevFiles = [i["fid"] for i in resultList]
        for i in thisYearPrevFiles:
            if prevFilesFidDelayDict[i] != 0:
                delayedCount += 1
        details = {"totalCount": result.count(), "delayedCount": delayedCount}
        response = {"status": "1", "details": details}
        return jsonify(response)
    else:
        return "POST not allowed"

    
    
@backendapp.route("/get_dept_stats_date_range",methods=["GET","POST"])
def get_dept_stats_date_range():
    if request.method == "GET":
        d = datetime.now()
        dept_id = request.args.get('dept_id')

        startYear = int(request.args.get('startYear'))
        startMonth = int(request.args.get('startMonth'))
        startDay = int(request.args.get('startDay'))
        endYear = int(request.args.get('endYear'))
        endMonth = int(request.args.get('endMonth'))
        endDay = int(request.args.get('endDay'))

        result = dept.find_one({"dept_id": dept_id})
        prevFiles = result["prevFiles"]

        prevFilesFid = []
        prevFilesFidDelayDict = {}
        for i in prevFiles:
            prevFilesFid.append(i["fid"])
            prevFilesFidDelayDict[i["fid"]] = i["delay"]

        d1 = datetime(year=startYear, month=startMonth, day=startDay, hour=0, minute=0, second=0,
                               microsecond=0)
        d2 = datetime(year=endYear, month=endMonth, day=endDay, hour=23, minute=59, second=59,
                               microsecond=999999)
        result = files.find({"fid": {"$in": prevFilesFid}, "timeCreated": {"$gte": d1, "$lte": d2}},
                            {"fid": True, "timeCreated": True, "_id": True})
        resultList = list(result)
        delayedCount = 0
        thisRangePrevFiles = [i["fid"] for i in resultList]
        for i in thisRangePrevFiles:
            if prevFilesFidDelayDict[i] != 0:
                delayedCount += 1
        details = {"totalCount": result.count(), "delayedCount": delayedCount}
        response = {"status": "1", "details": details}
        return jsonify(response)
    else:
        return "POST not allowed"



    
    
@backendapp.route("/get_dept_cmp_stats_current_month",methods=["GET","POST"])
def get_dept_cmp_stats_current_month():
    if request.method=="GET":
        d=datetime.now()
        dept_id = request.args.get('dept_id')

        result = dept.find_one({"dept_id": dept_id})
        prevFiles = result["prevFiles"]
        prevFilesFid = []
        prevFilesFidDelayDict={}
        for i in prevFiles:
            prevFilesFid.append(i["fid"])
            prevFilesFidDelayDict[i["fid"]]=i["delay"]

        thisMonthDays=calendar.monthrange(d.year, d.month)[1]

        d1 = datetime(year=d.year, month=d.month, day=1, hour=0, minute=0, second=0, microsecond=0)
        d2 = datetime(year=d.year, month=d.month, day=thisMonthDays, hour=23, minute=59, second=59, microsecond=999999)
        result = files.find({"fid":{"$in":prevFilesFid},"timeCreated":{"$gte":d1,"$lte":d2}},{"fid":True,"timeCreated":True,"_id":True})
        resultList = list(result)
        delayedCount = 0
        thisMonthPrevFiles = [i["fid"] for i in resultList]
        for i in thisMonthPrevFiles:
            if prevFilesFidDelayDict[i] != 0:
                delayedCount += 1

        details = {"totalCount":result.count(),"delayedCount":delayedCount}
        response = {"status":"1","details":details}
        return jsonify(response)
    else:
        return "POST not allowed"

    
    
@backendapp.route("/get_dept_cmp_stats_quarter",methods=["GET","POST"])
def get_dept_cmp_stats_quarter():
    if request.method=="GET":
        d=datetime.now()
        dept_id = request.args.get('dept_id')
        quarter = request.args.get('quarter')
        print("QUARTER TYPE : {}".format(type(quarter)))
        startMonth = quarterDetails[quarter][0]
        endMonth = quarterDetails[quarter][1]
        result = dept.find_one({"dept_id": dept_id})
        prevFiles = result["prevFiles"]
        prevFilesFid = []
        prevFilesFidDelayDict = {}
        for i in prevFiles:
            prevFilesFid.append(i["fid"])
            prevFilesFidDelayDict[i["fid"]] = i["delay"]
        print("PrevFilesFidDelayDict : {}".format(prevFilesFidDelayDict))
        startMonthDays=calendar.monthrange(d.year, startMonth)[1]
        endMonthDays=calendar.monthrange(d.year,endMonth)[1]

        print("PrevFilesFid : {}".format(prevFilesFid))
        d1 = datetime(year=d.year, month=startMonth, day=1, hour=0, minute=0, second=0, microsecond=0)
        d2 = datetime(year=d.year, month=endMonth, day=endMonthDays, hour=23, minute=59, second=59, microsecond=999999)
        print("D1 : {}".format(d1))
        print("D2 : {}".format(d2))
        
        result = files.find({"fid":{"$in":prevFilesFid},"timeCreated":{"$gte":d1,"$lte":d2}},{"fid":True,"timeCreated":True,"_id":True})
        resultList = list(result)
        #print("ResultList  : {}".format(resultList))
        delayedCount = 0
        thisQuarterPrevFiles = [i["fid"] for i in resultList]
        print("thisQuarterPrevFiles  : {}".format(thisQuarterPrevFiles))
        for i in thisQuarterPrevFiles:
            if prevFilesFidDelayDict[i] != 0:
                delayedCount += 1
        details = {"totalCount":len(resultList),"delayedCount":delayedCount}
        response = {"status":"1","details":details}
        print(response)
        return jsonify(response)
    else:
        return "POST not allowed"

    
    
@backendapp.route("/get_dept_cmp_stats_year",methods=["GET","POST"])
def get_dept_cmp_stats_year():
    if request.method == "GET":
        d = datetime.now()
        dept_id = request.args.get('dept_id')
        year = int(request.args.get('year'))

        result = dept.find_one({"dept_id": dept_id})
        prevFiles = result["prevFiles"]

        prevFilesFid = []
        prevFilesFidDelayDict = {}
        for i in prevFiles:
            prevFilesFid.append(i["fid"])
            prevFilesFidDelayDict[i["fid"]] = i["delay"]

        d1 = datetime(year=year, month=1, day=1, hour=0, minute=0, second=0,
                               microsecond=0)
        d2 = datetime(year=year, month=12, day=31, hour=23, minute=59, second=59,
                               microsecond=999999)
        result = files.find({"fid": {"$in": prevFilesFid}, "timeCreated": {"$gte": d1, "$lte": d2}},
                            {"fid": True, "timeCreated": True, "_id": True})
        resultList=list(result)
        delayedCount = 0
        thisYearPrevFiles = [i["fid"] for i in resultList]
        for i in thisYearPrevFiles:
            if prevFilesFidDelayDict[i] != 0:
                delayedCount += 1
        details = {"totalCount": result.count(), "delayedCount": delayedCount}
        response = {"status": "1", "details": details}
        return jsonify(response)
    else:
        return "POST not allowed"

    
    
@backendapp.route("/get_dept_cmp_stats_date_range",methods=["GET","POST"])
def get_dept_cmp_stats_date_range():
    if request.method == "GET":
        d = datetime.now()
        dept_id = request.args.get('dept_id')

        startYear = int(request.args.get('startYear'))
        startMonth = int(request.args.get('startMonth'))
        startDay = int(request.args.get('startDay'))
        endYear = int(request.args.get('endYear'))
        endMonth = int(request.args.get('endMonth'))
        endDay = int(request.args.get('endDay'))

        result = dept.find_one({"dept_id": dept_id})
        prevFiles = result["prevFiles"]

        prevFilesFid = []
        prevFilesFidDelayDict = {}
        for i in prevFiles:
            prevFilesFid.append(i["fid"])
            prevFilesFidDelayDict[i["fid"]] = i["delay"]

        d1 = datetime(year=startYear, month=startMonth, day=startDay, hour=0, minute=0, second=0,
                               microsecond=0)
        d2 = datetime(year=endYear, month=endMonth, day=endDay, hour=23, minute=59, second=59,
                               microsecond=999999)
        result = files.find({"fid": {"$in": prevFilesFid}, "timeCreated": {"$gte": d1, "$lte": d2}},
                            {"fid": True, "timeCreated": True, "_id": True})
        resultList = list(result)
        delayedCount = 0
        thisRangePrevFiles = [i["fid"] for i in resultList]
        for i in thisRangePrevFiles:
            if prevFilesFidDelayDict[i] != 0:
                delayedCount += 1
        details = {"totalCount": result.count(), "delayedCount": delayedCount}
        response = {"status": "1", "details": details}
        return jsonify(response)
    else:
        return "POST not allowed"


    
    
@backendapp.route("/get_emp_stats",methods=["GET","POST"]) #TEST
def get_emp_stats():
    if request.method == "POST":
        if "application/x-www-form-urlencoded" in request.headers["Content-Type"]:
            postData = request.form
        else:
            postData = request.get_json()
        print("postdata = {0}".format(postData))
        email_id = postData["email_id"]
        #print(email_id)
        results = emp_stats.find_one({"email_id":email_id})
        if results == None :
            response = {"status": "0", "details": "error"}
            return jsonify(response)
        currFiles = results["currFiles"]
        currFilesWithDelay = []
        for i in currFiles:
            delay = chk_delayed(i["fid"])
            #print("{0} --> {1}".format(i,delay))
            if delay[0] == None:
                delay[0] = 0
            if delay[1]==delay[2]:
                lastStep = True
            else:
                lastStep = False
            currFilesWithDelay.append({"fid":i["fid"],"timeArrived":i["timeArrived"],"delay":delay[0],"lastStep":lastStep})
        prevFiles = results["prevFiles"]
        incomingFiles = results["incomingFiles"]
        outgoingFiles = results["outgoingFiles"]
        details = {"currFiles":currFilesWithDelay,"prevFiles":prevFiles,"incomingFiles":incomingFiles,"outgoingFiles":outgoingFiles}
        response= {"status":"1","details":details}
        #print(response)
        return jsonify(response)
    else:
        return "GET is not allowed"

    
    
    
@backendapp.route("/get_emp_dashboard_stats",methods=["GET","POST"])
def get_emp_dashboard_stats():
    if request.method == "GET":
        email_id = request.args.get('email_id')
        #print(email_id)
        results = emp_stats.find_one({"email_id":email_id})
        if results == None :
            response = {"status": "0", "details": "error"}
            return jsonify(response)
        currFiles = results["currFiles"]
        currFilesWithDelay = 0
        for i in currFiles:
            delay = chk_delayed(i["fid"])
            #print("{0} --> {1}".format(i,delay))
            if delay[0] != None:
                currFilesWithDelay+=1
            #currFilesWithDelay.append({"fid":i["fid"],"timeArrived":i["timeArrived"],"delay":delay})
        prevFiles = results["prevFiles"]
        details = {"currFilesCount":len(currFiles),"currFilesDelayCount":currFilesWithDelay,"prevFilesCount":len(prevFiles)}
        response= {"status":"1","details":details}
        print(response)
        return jsonify(response)
    else:
        return "POST is not allowed"


    
    
def chk_delayed_rating(file):
    print(file)
    today = datetime.now().date()
    result = files.find_one({"fid":file})
    print("{} ----- {}".format(list(result), file))
    currDept = result["currDept"]
    expectedTimeline = result["expectedTimelineDuplicate"]
    expectedDate = expectedTimeline[currDept].date()
    print("{} ----- {}".format(expectedDate,today))
    if(expectedDate<today):
        return [int((today-expectedDate).days),currDept,result["lastDept"]]
    else:
        return [None,currDept,result["lastDept"]]

    
    
@backendapp.route("/get_dept_emp_data_for_rating",methods=["GET","POST"])
def get_dept_emp_data_for_rating():
    if request.method == "GET":
        dept_id = request.args.get('dept_id')
        employees = emp_stats.find({"dept_id":dept_id},{"email_id":True,"prevFiles":True,"_id":False})
        employees_list = list(employees)
        details=[]
        #print("EMP LIST {}".format(employees_list))
        for i in employees_list:
            #print("I --> {}".format(i))
            d={}
            d["email_id"] = i["email_id"]
            print(i["email_id"])
            emp_details = emp_data.find_one({"email_id":i["email_id"]},{"fname":True,"lname":True,"mno":True,"dept_id":True,"_id":False})
            dept_name = dept.find_one({"dept_id":emp_details["dept_id"]},{"dept_name":True,"_id":False})
            #print(name)
            d["name"]="{0} {1}".format(emp_details["fname"],emp_details["lname"])
            d["mno"]=emp_details["mno"]
            d["dept_name"]=dept_name["dept_name"]
            prevFiles = i["prevFiles"]
            prevFilesWithDelay = 0
            print("email_id for whom searching : ".format({d["email_id"]}))
            avgDelay = 0
            delaySum = 0
            count = 0
            for j in prevFiles:
                count += 1
                if j["delay"] != 0:
                    prevFilesWithDelay += 1
                    delaySum += j["delay"]
            if count != 0:
                avgDelay = delaySum/count
            d["prevFilesWithDelay"]=prevFilesWithDelay
            d["prevFilesCount"]=len(i["prevFiles"])
            d["avgDelay"]=avgDelay
            details.append(d)
        response = {"status": "1", "details": details}
        print(response)
        return jsonify(response)
    else:
        return "POST is not allowed"


    
    
@backendapp.route("/get_emp_data_for_rating",methods=["GET","POST"])
def get_emp_data_for_rating():
    if request.method == "POST":
        if "application/x-www-form-urlencoded" in request.headers["Content-Type"]:
            postData = request.form
        else:
            postData = request.get_json()
        email_id=postData['email_id']
        employee_stats = emp_stats.find_one({"email_id":email_id}, {"email_id": True, "dept_id":True,"prevFiles": True, "_id": False})

        details={}

        details["email_id"] = email_id
        details["dept_id"] = employee_stats["dept_id"]
        emp_details = emp_data.find_one({"email_id":email_id},{"fname":True,"lname":True,"mno":True,"dept_id":True,"_id":False})
        dept_name = dept.find_one({"dept_id":emp_details["dept_id"]},{"dept_name":True,"_id":False})

        details["name"]="{0} {1}".format(emp_details["fname"],emp_details["lname"])
        details["mno"]=emp_details["mno"]
        details["dept_name"]=dept_name["dept_name"]
        prevFiles = employee_stats["prevFiles"]
        prevFilesWithDelay = 0
        print("email_id for whom searching : ".format({details["email_id"]}))
        avgDelay = 0
        delaySum = 0
        count = 0
        for i in prevFiles:
            count += 1
            if i["delay"] != 0:
                prevFilesWithDelay += 1
                delaySum += i["delay"]
        if count != 0:
            avgDelay = delaySum/count
        details["prevFilesWithDelay"]=prevFilesWithDelay
        details["prevFilesCount"]=len(employee_stats["prevFiles"])
        details["avgDelay"]=avgDelay

        response = {"status": "1", "details": details}
        print(response)
        return jsonify(response)
    else:
        return "POST is not allowed"


@backendapp.route("/get_dept_employees",methods=["GET","POST"])
def get_dept_employees():
    if request.method == "GET":
        dept_id = request.args.get('dept_id')
        employees = emp_stats.find({"dept_id":dept_id},{"email_id":True,"_id":False})
        employees_list = list(employees)
        response = {"status": "1", "employees": employees_list}
        return jsonify(response)
    else:
        return "POST is not allowed"

    
    
@backendapp.route("/get_overall_stats",methods=["GET","POST"])
def get_overall_stats():
    if request.method == "GET":
        completedCount = files.find({"fileDone":True},{"fid":1,"_id":0}).count()
        currentProcessingCount = files.find({"fileDone":False},{"fid":1,"_id":0}).count()
        currentProcessingDelayCount = files.find({"fileDone":False,"delayed":True},{"fid":1,"_id":0}).count()
        details = {"completedCount":completedCount,"currentProcessingCount":currentProcessingCount,
                   "currentProcessingDelayCount":currentProcessingDelayCount}
        response = {"status":"1","details":details}
        return jsonify(response)
    else:
        return "POST method not allowed"


    
    
'''                                                      Department Comparison                                   '''

@backendapp.route("/get_dept_stats_comparison",methods=["GET","POST"])
def get_dept_stats_comparison():
    if request.method == "GET":
        pass
    else:
        return "POST method is not allowed"

    
'''                                                      Department Comparison                                   '''

'''                                                       ALL STATS                                             '''

'''                                                       ALL STATS                                             '''

'''                                                     CALENDAR                                                 '''

@backendapp.route("/get_calendar",methods=["GET","POST"])
def get_calendar():
    if request.method == "GET":
        lst = list(holidays.find({},{"dateDay":1,"description":1,"_id":0}))
        response = {"status":"1","holidays":lst}
        return jsonify(response)
    else:
        return ("POST not allowed")

    
    
@backendapp.route("/update_calendar",methods=["GET","POST"])
def update_calendar():
    print("Request method : {}".format(request.method))
    print("Request headers : {}".format(request.headers))
    if request.method == "POST":
        if "application/x-www-form-urlencoded" in request.headers["Content-Type"]:
            postData = request.form
        else:
            postData = request.get_json()

        print("PostData : {}".format(postData))
        for i,j in postData.items():
            print("{}  {}".format(i,j))
        #holidaysUpdate = postData.getlist("hh[]")
        holidays.delete_many({})
        for date, description in sorted(postData.items()):
            #print("{}  {}".format(date, name))
            holidays.insert_one({"dateDay":date,"description":description})
        response = {"status":"1","message":"Done"}
        return jsonify(response)
    else:
        return ("GET method not allowed")

'''                                                     CALENDAR                                                  '''

#-----------------------------tejas added routes-----------------------------------------------



# application types graph route

@backendapp.route("/get_applications_stats",methods=["GET","POST"])
def get_applications_stats():
    if request.method == "GET":
        
        applications = files.distinct("applicationType")
        details={}
        for i in applications :
            cnt={}
            cnt['processfcnt'] = files.find({"applicationType":i,"fileDone":False}).count() 
            cnt['delayfcnt'] = files.find({"applicationType":i,"delayed":True}).count() 
            cnt['completedfcnt'] = files.find({"applicationType":i,"fileDone":True}).count() 
            details[i]=cnt
            
        response = {"status":"1","message":details,"applist":applications}
        return jsonify(response)
    else:
        return ("Post method not allowed")







#--------------------------------------------Back-End End----------------------------------------
