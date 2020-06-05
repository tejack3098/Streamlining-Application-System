from datetime import datetime,timedelta
import pymongo
import  calendar

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
filetracker = myclient["filetracker"]
emp_stats= filetracker["emp_stats"]

all_emp = emp_stats.find({},{"email_id":1,"_id":0})
'''
for i in list(all_emp):
    incomingFiles = emp_stats.find_one({"email_id":i["email_id"]},{"incomingFiles":1,"_id":0})

    for fid,details in incomingFiles['incomingFiles'].items():
        print("{} {}".format(fid,details))
        incomingFiles['incomingFiles'][fid]["from"]="OLd therefore Nothing"
        incomingFiles['incomingFiles'][fid]["alert"]=False
    emp_stats.find_one_and_update({"email_id":i["email_id"]},{"$set":{"incomingFiles":incomingFiles['incomingFiles']}})
'''
incomingFiles = emp_stats.find_one({"email_id":"shaileshgupta596@gmail.com"},{"incomingFiles":1,"_id":0})
income = incomingFiles['incomingFiles']['incomingFiles']
print(income)
emp_stats.find_one_and_update({"email_id":"shaileshgupta596@gmail.com"},{"$set":{"incomingFiles":income}})
myclient.close()