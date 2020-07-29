import holidays as hd
import pymongo
from datetime import datetime,timedelta
from time import strptime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

filetracker = myclient["filetracker"]
holidays = filetracker["holidays"]
#d=datetime("2020-01-26")
'''
d=0
for date, name in sorted(hd.IND(years=datetime.now().year).items()):
    print("{}  {}".format(date,name))

    holidays.insert_one({"dateDay":str(date),"description":name})

holidays.create_index([("dateDay",pymongo.TEXT)])
print(list(holidays.list_indexes()))
'''
'''
def date_by_adding_business_days(from_date, add_days):
    business_days_to_add = add_days
    current_date = from_date.date()
    l = list(holidays.find({}, {"dateDay": True, "_id": False}))
    hh = [datetime.strptime(d['dateDay'],"%Y-%m-%d").date() for d in l]
    print(hh)
    while business_days_to_add > 0:
        current_date += timedelta(days=1)
        weekday = current_date.weekday()
        if current_date in hh:
            print(current_date)
            print("In hh")
            continue
        if weekday >= 5:  # sunday = 6
            continue
        business_days_to_add -= 1
    return current_date
'''

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
d = datetime.now()
print(date_by_adding_business_days(d,3))

myclient.close()