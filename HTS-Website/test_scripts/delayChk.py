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


delayMessage = "File {} at your desk is delayed by {} days!"

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

result = files.find({"fileDone":False},{"fid":True,"currEmp":True,"currDept":True,"_id":False})

#dept_count = 0

for i in result:
    fid = i["fid"]

    delay = chk_delayed(fid)
    d = datetime.now()
    t= d.timestamp()
    if delay != None:
        notifications.insert_one({"notificationID":i["currEmp"].split("@")[0]+str(t),"email_id": i["currEmp"], "message": delayMessage.format(fid, delay),"timeCreated":d,"read":False})
        mno_result = emp_data.find_one({"email_id": i["currEmp"]}, {"mno": True, "_id": False})
        mno = mno_result['mno']
        print(mno)
        delayUpdate = True
    else:
        delay = 0
        delayUpdate = False

    files.find_one_and_update({"fid":fid},{"$set":{"delayed":delayUpdate,"delayedDays":delay}})
#dept.find_one_and_update({"dept_id": i["dept_id"]}, {"$set": {"delayedCount": dept_count}})
myclient.close()