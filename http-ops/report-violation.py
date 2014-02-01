#!/usr/bin/env python
#
# Report a traffic violation on BTP Public eye website, and return the complaint number on success.
#
import requests
from bs4 import BeautifulSoup
import exifread

import argparse
import sys

def getEXIF(fname):
	f=open(fname,'r')
	exifDict = exifread.process_file(f)
	# exifDict['EXIF DateTimeOriginal']
	f.close()
	return exifDict

url = 'http://www.bangaloretrafficpolice.gov.in/PublicEye/PublicEyePost.aspx'

categories = {
	"defective-number-plate": "DEFECTIVE NUMBER PLATE|Y",
	"no-parking": "NO PARKING|N",
	"seat-belt": "NOT WEARING SEAT BELT|N",
	"one-way": "ONEWAY/NOENTRY|N",
	"footpath-parking": "PARKING ON FOOTPATH|N",
	"footpath-riding": "RIDING ON FOOTPATH|N",
	"no-helmet": "RIDING WITHOUT A HELMET|Y",
	"zerbra": "STOPPED ON ZEBRA CROSS/NEAR TRF LIGHT|N",
	"no-u-turn": "TAKING A U-TURN WHERE U-TURN IS PROHIBITED|N",
	"triple-riding": "TRIPLE RIDING|N",
	"mobile-phone": "USING MOBILEPHONE|N",
	"lane-discipline": "VIOLATING LANE DISCIPLINE|N",
	"wrong-parking": "WRONG PARKING|N",
}

# txtVehicleRegno, max length 12  
# txtDate in MMDDYYYY format
# ddlCategory is one of above
# ddlHours - 00 to 23
# ddlMinutes - 00 to 59
# txtVioPlace place of violation, 50 chars max
# txtRemark 3 rows 5 cols
# txtPersonName name of reporter, 50 chars max
# txtMobileno mobile number of reporter, max 12 chars numeric
# txtEmailid email address, max 40 chars
# fuImage, type file, size limit 200kB
# btnSubmit, set to "Submit"
#

parser = argparse.ArgumentParser()
#parser.add_argument("violation", help="Type of violation", type=str, choices=categories.keys())
args = parser.parse_args()

# Fire a GET request to get ASP.NET state. Public Eye website uses ASP.NET, so we need to accomodate
# it's quirks!
r = requests.get(url)

# Tips from http://stackoverflow.com/questions/14746750/post-request-using-python-to-asp-net-page
# on how to deal with ASP.NET stuff
#
soup = BeautifulSoup(r.text)
viewstate = soup.select("#__VIEWSTATE")[0]['value']
eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']

values = {'btnSubmit':'Submit' }
values['__VIEWSTATE']=viewstate
values['__EVENTVALIDATION']=eventvalidation

values['txtVehicleRegno']='KA40O1071'
values['txtDate']='01/17/2014'
values['txtVioPlace']='Richmond road, after the mosque.'
values['ddlCategory']="RIDING ON FOOTPATH|N"
values['ddlHours']='10'
values['ddlMinutes']='55'
values['txtRemark']='Riding on footpath to get ahead in traffic'
values['txtPersonName']='Shree Kumar'
values['txtMobileno']='9449835848'
values['txtEmailid']='shree.shree@gmail.com'

# Note : the below is needed too!
values['hdnToday']='01/28/2014'

# Note : not sure abt the following one!
values['hdn_MsgStatusTime']='7 days'

files={'fuImage':open('footpath-ka40-o1071.jpg','rb')}

# Now, fire the real POST request that will submit the complaint
r = requests.post(url, data=values, files=files)
print r.text
f=open('out.html', 'w')
print >>f,r.text
f.close()
