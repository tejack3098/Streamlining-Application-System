import pymongo
from datetime import datetime
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
    notifications = filetracker["notifications"]
except:
    print("MongoDB error: notifications Table might not exist")
    notifications=None

import requests
import smtplib, ssl

delayMessage = "File {} at your desk is delayed by {} days!"
def send_sms(receiver,fid,delay):
    url = "https://www.fast2sms.com/dev/bulk"
    payload = "sender_id=FSTSMS&message="+delayMessage.format(fid,delay)+"&language=english&route=p&numbers=" + receiver  # 7506303749,7045815501"
    headers = {
        'authorization': "OxFvZsGpqEL3eHnMXr4NgBPbdomt7cDV1k2aYl8CzTKIi0Aj9QYnKt2Z1BDhvFyHicSXj6wfUxeIsb8q",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)


def send_mail(receiver,fid,delay):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "chavanrachit16e@student.mes.ac.in"
    password = 'chavan@123'
    receiver_email = receiver  # "kadusaswit16e@student.mes.ac.in"
    message = """\
    Subject: File delay

    """+delayMessage.format(fid,delay)

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        # TODO: Send email here
        server.sendmail(sender_email, receiver_email, message)
        print("SENT TO {}".format(receiver_email))
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    # finally:
    # server.quit()

def chk_delayed(file):
    try:
        today = datetime.now().date()
        result = files.find_one({"fid":file})
        currDept = result["currDept"]
        print("{} currdept {}".format(file,currDept))
        expectedTimeline = result["expectedTimelineDuplicate"]
        expectedDate = expectedTimeline[currDept].date()
        print("{} + {}".format(expectedDate,today))
        if(expectedDate<today):
            return int((today-expectedDate).days)
        else:
            return None

    except:
        pass
result = files.find({"fileDone":False},{"fid":True,"currEmp":True,"currDept":True,"delayNotificationSent":True,"_id":False})

#dept_count = 0

for i in result:
    fid = i["fid"]

    delayNotificationSent = i["delayNotificationSent"]
    '''i["delayNotificationSent"] = ["hello"]
    if (delayNotificationSent == None):
        print("message sent")
    else:
        print("not send")'''
    delay = chk_delayed(fid)
    d = datetime.now()
    t= d.timestamp()
    if delay != None:
        if (delayNotificationSent == None):
            notifications.insert_one({"notificationID":i["currEmp"].split("@")[0]+str(t).split('.')[0],"email_id": i["currEmp"], "message": delayMessage.format(fid, delay),"timeCreated":d,"read":False})
            mno_result = emp_data.find_one({"email_id": i["currEmp"]}, {"mno": True, "_id": False})
            mno = mno_result['mno']
            print(mno)
            delayUpdate = True

            #dept_count+=1

            send_mail(i["currEmp"],fid,delay)#email pass i["currEmp"]
            send_sms(mno,fid,delay)#sms pass mno

            emplst = {i["currEmp"]:d}
            files.find_one_and_update({"fid": fid}, {"$set": {"delayNotificationSent": emplst}})

        else:
            '''print(delayNotificationSent[i["currEmp"]].date())
            print(d.date())'''

            if i["currEmp"] in delayNotificationSent:
                if(d.date()>delayNotificationSent[i["currEmp"]].date()):
                    notifications.insert_one(
                        {"notificationID": i["currEmp"].split("@")[0] + str(t).split('.')[0], "email_id": i["currEmp"],
                         "message": delayMessage.format(fid, delay), "timeCreated": d, "read": False})
                    mno_result = emp_data.find_one({"email_id": i["currEmp"]}, {"mno": True, "_id": False})
                    mno = mno_result['mno']
                    print(mno)
                    delayUpdate = True

                    # dept_count+=1

                    send_mail(i["currEmp"], fid, delay)  # email pass i["currEmp"]
                    send_sms(mno, fid, delay)  # sms pass mno

                    emplst = {i["currEmp"]: d}
                    files.find_one_and_update({"fid": fid}, {"$set": {"delayNotificationSent": emplst}})
                else:
                    delayUpdate = True

            else:
                notifications.insert_one(
                    {"notificationID": i["currEmp"].split("@")[0] + str(t).split('.')[0], "email_id": i["currEmp"],
                     "message": delayMessage.format(fid, delay), "timeCreated": d, "read": False})
                mno_result = emp_data.find_one({"email_id": i["currEmp"]}, {"mno": True, "_id": False})
                mno = mno_result['mno']
                print(mno)
                delayUpdate = True

                # dept_count+=1

                send_mail(i["currEmp"], fid, delay)  # email pass i["currEmp"]
                send_sms(mno, fid, delay)  # sms pass mno

                emplst = delayNotificationSent
                emplst[i["currEmp"]] = d
                files.find_one_and_update({"fid": fid}, {"$set": {"delayNotificationSent": emplst}})

    else:
        delay = 0
        delayUpdate = False

    files.find_one_and_update({"fid":fid},{"$set":{"delayed":delayUpdate,"delayedDays":delay}})
#dept.find_one_and_update({"dept_id": i["dept_id"]}, {"$set": {"delayedCount": dept_count}})
myclient.close()