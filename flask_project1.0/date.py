from pytz import utc
from pytz import timezone
from datetime import datetime

cst_tz = timezone('Asia/Shanghai')
utc_tz = timezone('UTC')

now = datetime.now().replace(tzinfo=cst_tz)
#local_dt = cst_tz.localize(now, is_dst=None)
utctime = now.astimezone(utc)

print ("now   : %s"%now)
print ("format: %s"%now.strftime('%Y-%m-%d %H:%M:%S'))
print ("utc   : %s"%utctime)

utcnow = datetime.utcnow()
utcnow = utcnow.replace(tzinfo=utc_tz)
china = utcnow.astimezone(cst_tz)

print ("utcnow: %s"%utcnow)
print ("format: %s"%utcnow.strftime('%Y-%m-%d %H:%M:%S'))
print ("china : %s"%china)