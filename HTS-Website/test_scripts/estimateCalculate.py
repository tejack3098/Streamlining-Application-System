import pymongo
import pandas as pd
import math
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
    estimateTime = filetracker["estimateTime"]
except:
    print("MongoDB error: estimateTime Tbale might not exist")
    estimateTime = None

file = pd.read_csv("estimateCSV/data.csv")

dic = {}
application = file["apt"].unique()
stages = file["sname"].unique()
for i in application:
    for j in stages:
        filter_data =  file[(file["apt"]==i)& (file["sname"]==j)]
        #print(filter_data)
        #lst = [math.ceil(filter_data["tat"].mean()),math.ceil(filter_data["delay"].mean())]
        lst = filter_data["tat"].mean()+filter_data["delay"].mean()
        dic[(i,j)]=math.ceil(lst)

        estimateTime.insert_one({"appid": i, "dept_id": "0{}".format(str(j)), "estimateDays": int(math.ceil(lst))})
print(dic)
myclient.close()