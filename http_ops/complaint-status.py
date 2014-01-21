#!/usr/bin/env python
#
# Query BTP Public eye website, and report status for a complaint number.
#
import requests
from bs4 import BeautifulSoup

import argparse
import sys

# Complaint Number
parser = argparse.ArgumentParser()
parser.add_argument("complaintNumber", help="Complaint number of a previously reported violation. e.g. 6891")
args = parser.parse_args()
complaintNumber = args.complaintNumber

url = 'http://www.bangaloretrafficpolice.gov.in/PublicEye/ComplaintStatus.aspx'

# Fire a GET request to get ASP.NET state. Public Eye website uses ASP.NET, so we need to accomodate
# it's quirks!
r = requests.get(url)

# Tips from http://stackoverflow.com/questions/14746750/post-request-using-python-to-asp-net-page
# on how to deal with ASP.NET stuff
#
soup = BeautifulSoup(r.text)
viewstate = soup.select("#__VIEWSTATE")[0]['value']
eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']

# Now, fire the real POST request that will return the data
values = {'txtCompno': '6891', 'btnSubmit':'Submit' }
values['__VIEWSTATE']=viewstate
values['__EVENTVALIDATION']=eventvalidation
r = requests.post(url, data=values)

# Extract & display the complaint data
#
#print soup.select('#divRegno')
#print soup.select('#divVtype')
#print soup.select('#divPremarks')
#print soup.select('#divRdate')
#print soup.select('#divVdateTm')
#
soup = BeautifulSoup(r.text)
attribs = [ ("Reg No   ", 'Regno'), 
            ("Violation", 'Vtype'), 
            ("Date     ", 'Rdate'),
            ("Time     ", 'VdateTm'),
            ("Remarks  ", 'Premarks'), 
          ]
for attr in attribs:
	n = soup.select('#div%s'%(attr[1]))
	val = n[0].text
	print "%s: %s"%(attr[0], val)
