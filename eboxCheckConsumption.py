from bs4 import BeautifulSoup
import urllib
import requests
import json
from datetime import date
import re
import os
from twilio.rest import Client

####constants ####
#ebox credentials
eboxUsername = 'InsertCredentialsHere'
eboxPassword = 'InsertCredentialsHere'
#twilio credentials
twilioAccount_sid = 'InsertCredentialsHere' 
twilioAuth_token = 'InsertCredentialsHere' 
twilioFromNumber = "+InsertNumberHere"
twilioToNumber = "+InsertNumberHere"


####Get Current Usage#####

#get session cooke
initialPage = urllib.urlopen('https://client.ebox.ca')
phpSessionCookie = initialPage.headers.items()[0][1].split(';')[0]

#get csrf token
btInitPage = BeautifulSoup(initialPage.read(),"lxml")
csrfTokenTag = btInitPage.find(attrs={"name": "_csrf_security_token"})['value']

#login
cookies = {phpSessionCookie.split('=')[0]: phpSessionCookie.split('=')[1]}
formData = {'usrname': eboxUsername, 'pwd': eboxPassword, '_csrf_security_token':csrfTokenTag}
postCredentials = requests.post('https://client.ebox.ca/login', cookies=cookies, data=formData)

#get current usage
myUsage = requests.get('https://client.ebox.ca/myusage', cookies=cookies)
btMyUsage = BeautifulSoup(myUsage.text ,"lxml")
usageSummary = btMyUsage.find("div", class_="usage_summary")
consumption = usageSummary.contents[1].string
timeleft = usageSummary.contents[3].contents[2].string

###Format Raw Data Usage######
#cleanup numbers extracted from webpage
def extractNumbersFromString(initialString,cleanNumers):
    for t in initialString.split():
        try:
            cleanNumers.append(float(t))
        except ValueError:
            pass

consumptionClean = []
extractNumbersFromString(consumption,consumptionClean)

timeleftClean = []
extractNumbersFromString(timeleft,timeleftClean)

strDataConsumed = "%.2f / %.2f Go" % (consumptionClean[0], consumptionClean[1])
strDayLeft =  "%d days left" %  (timeleftClean[0])

##### Diplay data usage ####
print strDataConsumed
print strDayLeft

#send SMS
def SendSMS(textToSend):
    client = Client(twilioAccount_sid, twilioAuth_token)
    client.api.account.messages.create(
        to=twilioToNumber,
        from_=twilioFromNumber,
        body= textToSend)

SendSMS(strDataConsumed + "\n" + strDayLeft)

#act on the data
isBusted = False
if consumptionClean[0] >= consumptionClean[1]:
    print "limit is busted!"
    isBusted = True
else:
    print "limit is ok"

if isBusted == True:
    print "Buy data block"
    SendSMS("Buying new data block")
    todays_date = date.today()

    #get block CSRF token
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    jsonContainingCsrf = requests.get("https://client.ebox.ca/ajax/options/bloc/"+str(todays_date.year)+"/"+str(todays_date.month), cookies=cookies, headers=headers)
    csrfTokenTag2 = re.search("_csrf_security_token.+",jsonContainingCsrf.json()['content']).group(0).split('"')[2]

    #send request to update blocks
    formData = {'year': str(todays_date.year), 'month': str(todays_date.month), '_csrf_security_token':csrfTokenTag2, 'optionTransaction':'upgrade', 'chosen_bloc':'5', 'recurring': 0, 'iread':'yes', 'pwd': eboxPassword, 'mode':'execute'}
    postBuyBlock = requests.post("https://client.ebox.ca/ajax/options/bloc/"+str(todays_date.year)+"/"+str(todays_date.month), cookies=cookies, data=formData, headers=headers)
    print postBuyBlock.status_code


