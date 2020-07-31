import pymongo
from datetime import datetime,timedelta


myclient = pymongo.MongoClient("mongodb://localhost:27017/")

if "filetracker" not in myclient.list_database_names():
    filetracker = myclient["filetracker"]

    files = filetracker["files"]
    files.insert_one({"fid":"6956570088822","applicationType":None,"timeCreated":None,\
                      "digital":False,"fileExtension":None,
                      "fileDone":None,"currDept":None,"currEmp":None,"prevDept":None,"prevEmp":None,"scanned":False,"lastScanTime":None,"delayed":None,\
                      "delayedDays":0,"expectedTimeline":[],"expectedTimelineDuplicate":[],\
                      "stageList":[],"firstDept":None,"lastDept":None,"delayNotificationSent":None})

    applications = filetracker["applications"]
    applications.insert_one({"appname":None,"appid": None, "timeCreated": None,"lastDept": None, "stageList": []})

    employees = filetracker["emp_data"]
    employees.insert_one({"email_id": "1@g.com", "password": "123", "fname": "Tejack", "lname": "Beer", "dept_id": "bevada",
                          "date_created": None})

    employees_stats = filetracker["emp_stats"]
    employees_stats.insert_one({"email_id": "1@g.com","dept_id":"bevada","count":0,"incomingFiles":{},"outgoingFiles":{},"currFiles":[],"prevFiles":[]})

    dept = filetracker["dept"]
    dept.insert_one({"dept_id": None,"dept_name":None,"timeCreated": None,"count":0,"delayedCount":0,"completedCount":0,"currFiles":[],"delayedFiles":[],"prevFiles":[]})

    estimateTime = filetracker["estimateTime"]
    estimateTime.insert_one({"appid": None, "dept_id": None, "estimateDays": None})

    notifications = filetracker["notifications"]
    notifications.insert_one({"notificationID":None,"email_id": None, "message": None, "timeCreated": None, "read": False})

    holidays = filetracker["holidays"]
    holidays.insert_one({"dateDay": "", "description": ""})

    adminInbox = filetracker["adminInbox"]
    adminInbox.insert_one({"notificationID":None,"emp_id":None,"message": None, "timeCreated": None, "read": False})

    files.create_index([("fid",pymongo.HASHED)])
    files.create_index([("timeCreated",pymongo.HASHED)])
    applications.create_index([("appid",pymongo.HASHED)])
    employees.create_index([("email_id",pymongo.HASHED)])
    employees_stats.create_index([("email_id",pymongo.HASHED)])
    dept.create_index([("dept_id",pymongo.HASHED)])
    notifications.create_index([("email_id", pymongo.HASHED)])
    notifications.create_index([("notificationID", pymongo.HASHED)])
    holidays.create_index([("dateDay", pymongo.TEXT)])
    adminInbox.create_index([("email_id", pymongo.HASHED)])
    adminInbox.create_index([("notificationID", pymongo.HASHED)])

    print(files.list_indexes())
    print(applications.list_indexes())
    print(employees.list_indexes())
    print(employees_stats.list_indexes())


def createEntry():
    filetracker = myclient["filetracker"]
    files = filetracker["files"]
    applications = filetracker["applications"]
    employees = filetracker["emp_data"]
    employees_stats = filetracker["emp_stats"]
    dept = filetracker["dept"]
    estimateTime = filetracker["estimateTime"]
    notifications = filetracker["notifications"]
    holidays = filetracker["holidays"]
    adminInbox = filetracker["adminInbox"]

    files.insert_one({"fid": "6956570088822", "applicationType": None, "timeCreated": None, \
                      "fileDone": None, "currDept": None, "currEmp": None,"prevDept":None,"prevEmp":None,"scanned":False, "delayed": None, \
                      "stageList": [],"firstDept":None,"lastDept":None,"delayNotificationSent": None})

    applications.insert_one({"appname":None,"appid": None, "timeCreated": None,"lastDept": None, "stageList": []})

    employees.insert_one({"email_id": "1@g.com", "password": "123", "fname": "Tejack", "lname": "Beer", "dept_id": "bevada", "date_created": None})

    employees_stats.insert_one(
        {"email_id": "1@g.com", "dept_id": "bevada", "incomingFiles": {}, "outgoingFiles": {}, "currFiles": [],
         "prevFiles": []})


    dept.insert_one({"dept_id": None,"dept_name":None,"timeCreated": None,"count":0,"delayedCount":0,"completedCount":0,"currFiles":[],"delayedFiles":[],"prevFiles":[]})


    estimateTime.insert_one({"appid": None, "dept_id": None, "estimateDays": None})

    notifications.insert_one({"notificationID":None,"email_id": None, "message": None, "timeCreated": None, "read": False})


    holidays.insert_one({"dateDay": "", "description": ""})


    adminInbox.insert_one({"notificationID": None, "emp_id": None, "message": None, "timeCreated": None, "read": False})

    files.create_index([("fid", pymongo.HASHED)])
    files.create_index([("timeCreated", pymongo.HASHED)])
    applications.create_index([("appid", pymongo.HASHED)])
    employees.create_index([("email_id", pymongo.HASHED)])
    employees_stats.create_index([("email_id", pymongo.HASHED)])
    dept.create_index([("dept_id", pymongo.HASHED)])
    notifications.create_index([("email_id", pymongo.HASHED)])
    notifications.create_index([("notificationID", pymongo.HASHED)])
    holidays.create_index([("dateDay", pymongo.TEXT)])
    adminInbox.create_index([("email_id", pymongo.HASHED)])
    adminInbox.create_index([("notificationID", pymongo.HASHED)])

    return True
def chk_delayed(file):
    today = datetime.now().date()
    result = files.find_one({"fid":file})
    currDept = result["currDept"]
    expectedTimeline = result["expectedTimeline"]
    expectedDate = expectedTimeline[currDept].date()

    if(expectedDate<today):
        return int((today-expectedDate).days)
    else:
        return None

#createEntry()
'''
def least_file_emp(dept_id):
    print(dept_id)
    results = emp_stats.find({"dept_id": dept_id}, {"email_id": True, "count": True, "_id": False})
    resultsDict = {}
    for i in results:
        resultsDict[i["email_id"]] = i["count"]
    print(resultsDict)
    #resultsDict.sort()
    Dic = {k: v for k, v in sorted(resultsDict.items(), key=lambda item: item[1])}
    print(Dic)
    print(Dic[0])
'''
filetracker = myclient["filetracker"]
files = filetracker["files"]

adminInbox = filetracker["adminInbox"]
adminInbox.insert_one({"notificationID":None,"emp_id":None,"message": None, "timeCreated": None, "read": False})
adminInbox.create_index([("email_id", pymongo.HASHED)])
adminInbox.create_index([("notificationID", pymongo.HASHED)])

print(list(adminInbox.list_indexes()))
myclient.close()