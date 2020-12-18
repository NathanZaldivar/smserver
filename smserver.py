#! /usr/bin/python3
from twilio.rest import Client
from datetime import date
from datetime import datetime
import time
import threading
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import schedule, os, signal

'''
Made by Nathan Zaldivar aka Rye.

Github: https://github.com/NathanZaldivar
Linkedin: https://www.linkedin.com/in/nathan-zaldivar-10853a140/


installation instructions can be found on the github page.
https://github.com/NathanZaldivar/smserver
'''


account_sid = 'ACCOUNT SID GOES HERE'
auth_token = 'AUTH TOKEN GOES HERE'
phone_number = '+1' + 'YOUR PHONE NUMBER GOES HERE IN'
twilio_phone_number = '+1' + 'YOUR TWILIO PHONE NUMBER GOES HERE'
IPV4 = 'YOUR COMPUTERS PRIVATE IPV4 GOES HERE' # type ifconfig in terminal (ipconfig for windows) if you're unsure what yours is.

help = '''

\ncommands:

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
'''

# Event Handler, contains all functions used to handle the management of events.
class Event_Handler:
    def __init__(self, memory):
        self.memory = memory
        self.events = {}


    def add_event(self, new_event, time):
        with open(self.memory, 'a') as events:
            events.write(new_event + '|' + time + '\n')


    def remove_event(self, event_to_remove):
        with open(self.memory) as f:
            lines = f.readlines()

        with open(self.memory, 'w') as events:
            for line in lines:
                if event_to_remove not in line.strip('\n'):
                    events.write(line)


    def event_parser(self):
        self.events = {}
        with open(self.memory) as events:
            for i in events.readlines():
                self.events.update({key:value for key, value in [i.strip().split('|')]})

    def sms_send(self, message):
        client.messages.create(to=phone_number, from_=twilio_phone_number,body=message)

    def event_checker(self):
        print('Running cycle')
        self.event_parser()
        today = date.today()
        for i in self.events.keys():
            due_date = self.events[i].split()
            if today.strftime('%m-%d-%Y') == due_date[1]:
                self.sms_send('\n\n{} event today\n date:{} time:{}'.format(i, due_date[0], due_date[1]))

# background process, can be checked with .check_background .
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

# flask server for reciving API requests from twilio.
# i know this isn't the prettiest, will fix later.
app = Flask(__name__)
@app.route('/sms', methods=['GET', 'POST'])
def server():
    message = request.values.get('Body', None)
    resp = MessagingResponse()
    if '.remove' in message:
        value = message.split()
        if value[1] not in Handle.events:
            resp.message('event not in memory')
        else:
            Handle.remove_event(value[1])
            resp.message('\n\n\nevent: {} was removed.'.format(value[1]))
    elif '.events' in message:
        Handle.event_parser()
        total = ''.join(f'\n{x} : {y}' for x, y in zip(Handle.events.keys(), Handle.events.values()))
        resp.message(total)
    elif '.status' in message:
        resp.message('Servers up!')
    elif '.help' in message:
        resp.message(help)
    elif '.add' in message:
        value = message.split(' ', 2)
        Handle.add_event(value[1], value[2])
        resp.message('added event {} to memory, for time: {}.'.format(value[1], value[2]))
    elif '.force_parse' in message:
        Handle.event_parser()
        resp.message('Done!')
    elif 'force_check' in message:
        Handle.event_checker()
        resp.message('Done!')
    elif '.check_background' in message:
        if b.is_alive():
            resp.message('Background is up')
        else:
            resp.message('ERROR something went wrong')
    elif '.force_quit' in message:
        pid = os.getpid()
        os.kill(pid, signal.SIGKILL)
    else:
        resp.message('unkown command, .help for commands')

    return str(resp)


if __name__ == '__main__':
    client = Client(account_sid, auth_token)
    Handle = Event_Handler('events.txt')
    b = threading.Thread(name='background_scheduler', target=background_scheduler)
    b.start()
    # You can change the port and host here. Debug should remain off as it makes your server vulnerable to this exploit : https://www.rapid7.com/db/modules/exploit/multi/http/werkzeug_debug_rce/
    app.run(port=59999, debug=False, host=IPV4)
