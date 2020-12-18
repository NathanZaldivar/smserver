# smserver

smserver is an event handler that uses SMS messaging. smserver uses Twilio and flask.


**Requirements**

5 main things you will need for smserver to work:

* Twilio account sid
* Twilio auth token
* a working phone number
* a Twilio bought phone number
* Connection to the internet

Creating a Twilio account is simple and easy, you will need to verify a phone number for your account, make sure you verify the phone number that will be the receiving number for the server, smserver can only send to one verified number, to increase this you can upgrade your Twilio account for $20 a month subscription.

_creating a Twilio account_

visit : https://www.twilio.com/try-twilio

once you verify your account and phone number you will need to grab 3 things the account sid, auth token, and a Twilio phone number.

the auth token and sid can be found here once you log in: https://www.twilio.com/console

next is to get a phone number, these are very cheap costing $1 per number and the SMS messaging fees are based on contents being sent, I've designed smserver to reduce the cost to a minimum but keep in mind that each SMS message sent by the server will cost an average of 0.007 cents, the good thing is that Twilio trial account gives you $15 which will last a while.

Twilio phone numbers can be found here : https://www.twilio.com/console/phone-numbers/search

it's recommended to get a phone number that is closest to your region to cut cost.

**Installation**

Download the zip file from the newest release, unzip and then run:

```
python3 -m pip install -r requirements.txt
```

this will download the required modules for smserver.

next is to paste the required info into smserver.py, open smserver with a text editor preferably an IDE but notepad will work.
paste the **account sid**, **auth token**, **your phone number**, **Twilio phone number**, and your **private IPv4 for the machine you're running the server on**.

Like so:

```
account_sid = 'AC53-XXXXXXXXXXXXXXXXXXXX-XXXXXXXXXX'

auth_token = '5c2e-XXXXXXXXXXXXXXX-XXXXXXXXXX'

phone_number = '+1' + '7044444444'

twilio_phone_number = '+1' + '9488888888'

IPv4 = '192.168.0.0'
```

once you do this you can save and close.

_Port fowarding_

The next and last step is to port forward to 59999 to the IPv4 of your machine for protocol TCP, this can be done by opening your router's settings and doing it there. if you're unfamiliar with port forwarding a guide can be found here : https://www.howtogeek.com/66214/how-to-forward-ports-on-your-router/
be sure to set your ip of your machine to static, the guide goes over this in detail.

once this is done you can run smserver.py, then send the command .status to your Twilio phone number from your verified phone number to check if it's up!


_running in the background_

smserver does not run well in the background while receiving messages still works the event checker will not, it's recommended that if plan to background smserver to do so with nohub, nohup can be installed with : 
```
apt-get install nohup
```
and then running
```
nohub python3 smserver.py &
```
**Features**

smserver handles both receiving, adding, removing, and alerting events to your phone. all commands are shown here :

```
commands:

.events : prints all events

.status : prints server status

.help : prints this message

.remove  : removes a event from memory
  
.add   : adds a event to memory, event name must contain no spaces, time must be in HOUR:MINam/pm format and date must be in month-day-year, so an example would be : .add dentist_appointment 3:40PM 10-02-2020

Debug:
.force_parse : forces the parse function

.force_check : forces the check function

.check_background : check background thread

.force_quit : stops the server
```

_background_scheduler_

the event checker is a background process that every 12 hours checks if an event is coming up, sending you a message if it's due. this can be changed by editing smserver.py under the background_scheduler function:
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
