# smserver

smserver is a event handler that uses sms messaging. smserver uses twilio and flask.


**Requriments**

5 main things you will need for smserver to work:

* twilio account sid
* twilio auth token
* a working phone number
* a twilio bought phone number
* connection to the internet

Creating a twilio acount is simple and easy, you will need to verify a phone number for your account, make sure you verify the phone number that will be the reciving number for the server, smserver can only send to one verifyed number, to increase this you can upgrade your twilio acount for $20 a month subcription.

_creating a twilio account_

visit : https://www.twilio.com/try-twilio

once you verify your account and phone number you will need to grab 3 things the account sid, auth token, and a twilio phone number.

the auth token and sid can be found here once you login : https://www.twilio.com/console

next is to get a phone number, these are very cheap costing $1 per number and the sms messeging fees are based on contents beeing sent, ive desighned smserver to reduce cost to a minimum but keep in mind that each sms message sent by the server will cost a avaerage of 0.007 cents, the good thing is that twilio trail acount gives you $15 which will last a while.

twilio phone numbers can be found here : https://www.twilio.com/console/phone-numbers/search

is recomended to get a phonenumber that is closest to your region to reduce cost.

**Installation**

Download the zip file from the newest release, unzip and then run:

```
python3 -m pip install -r requirements.txt
```

this will download the required modules for smserver.

next is to paste the requred info into smserver.py, open smserver with a text editor perfearbly a IDE but notepad will work.
paste the **account sid**, **auth token**, **your phone number**, **twilio phone number**, and your **private IPV4 for the machine your running the server on**.

Like so:

```
account_sid = 'AC53-XXXXXXXXXXXXXXXXXXXX-XXXXXXXXXX'

auth_token = '5c2e-XXXXXXXXXXXXXXX-XXXXXXXXXX'

phone_number = '+1' + '7044444444'

twilio_phone_number = '+1' + '9488888888'

IPV4 = '192.168.0.0'
```

once you do this you can save and close.

_Port fowarding_

The next and final step is to port foward to 59999 to the IPV4 of your machine for protocol TCP, this can be done by opening your routers settings and doing it there. if you're unfimilar with port fowarding a guide can be found here : https://www.howtogeek.com/66214/how-to-forward-ports-on-your-router/
be sure to set your ip of your machine to static, the guide goes over this in detail.

once this is done you can run smserver.py, then send the command .status to your twilio phone number from your verified phone number to check if its up!


_running in the background_

smserver does not run well in the background while reciving messages still works the event checker will not, its recomended that if plan to background smserver to do so with with nohub, nohup can be installed with : 
```
apt-get install nohup
```
**Features**

smserver handles both reciving, adding, removing and alerting events to your phone. all commands are shown here :

```
commands:

.events : prints all events

.status : prints server status

.help : prints this message

.remove <event name> : removes a event from memory
  
.add <event_name> <time> <date>: adds a event to memory, event name must contain no spaces, time must be in HOUR:MINam/pm format and date must be in month-day-year, so an example would be : .add dentist_appointment 3:40PM 10-02-2020

Debug:
.force_parse : forces the parse function

.force_check : forces the check function

.check_background : check background thread

.force_quit : stops the server
```

_background_scheduler_

the event checker is a background process that every 12 hours checks if an event is comming up, sending you a message if its due. this can be changed by editing smserver.py under the background_scheduler funtion:
```
def background_scheduler():
    schedule.every(12).hours.do(Handle.event_checker)
    # By default event_checker is ran every 12 hours but you can uncomment the lines below to suit your needs. remember to comment or delete the line above if you do.

    #schedule.every(12).seconds.do(Handle.event_checker)
    #schedule.every(12).minutes.do(Handle.event_checker)
    #schedule.every().day.at("14:30").do(Handle.event_checker)
    #schedule.every(5).to(10).minutes.do(Handle.event_checker)
    while 1:
        schedule.run_pending()
        time.sleep(1)
```

_changing port and host_

changing the port or host can be done on the last line of smserver.
```
app.run(port=59999, debug=False, host=IPV4)
```

