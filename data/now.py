from datetime import datetime

now = datetime.now()

print("now date and time : " + str(now))
print("now year : " + str(now.year))
print("now month : " + str(now.month))
print("now day : " + str(now.day))
print("now hour : " + str(now.hour))
print("now minute : " + str(now.minute))
print("now second : " + str(now.second))
print("now date : {}-{}-{} ".format(now.year, now.month, now.day))