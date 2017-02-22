from subprocess import call
from flask import Flask, request, redirect
from twilio import twiml
from twilio.rest import TwilioRestClient
import serial, sys, json
import OSC

#ngrok http -subdomain=uarm 5000

app = Flask(__name__)

ACCOUNT_SID = "ACf540e9c22c3e93d6bbd74c0af36b5c2d"
AUTH_TOKEN = "5ce7b32f70cd243c03bf9cdb14df3dda"

#client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

c = OSC.OSCClient()
c.connect(('127.0.0.1', 12000))

c2 = OSC.OSCClient()
c2.connect(('127.0.0.1', 12001))


#open("uarm.txt", 'w').close()


def print_to_console(str):
	call(["echo", str])


def write_to_txt(str):
    txt = open("uarm.txt", "a")
    txt.write(str)
    txt.close()

#print_to_console()

@app.route("/", methods=['GET'])
def index():
	return("Sup")


@app.route("/arm1", methods=['GET','POST'])
def sms1():

    msg = request.form['Body']
    
    

    if msg == "UP" or msg == "up" or msg == "Up":
        body = "up"
        message = "Go Red Team! Arm 1 Moving Up!"
    elif msg == "DOWN" or msg == "down" or msg == "Down":
        body = "down"
        message = "Go Red Team! Arm 1 Moving Down!"
    elif msg == "LEFT" or msg == "left" or msg == "Left":
        body = "left"
        message = "Go Red Team! Arm 1 Moving Left!"
    elif msg == "RIGHT" or msg == "right" or msg == "Right":
        body = "right"
        message = "Go Red Team! Arm 1 Moving Right!"
    elif msg == "FORWARD" or msg == "forward" or msg == "Forward":
        body = "forward"
        message = "Go Red Team! Arm 1 Moving Forward!"
    elif msg == "BACK" or msg == "back" or msg == "Back":
        body = "back"
        message = "Go Red Team! Arm 1 Moving Back!"
    elif msg == "CLOCKWISE" or msg == "clockwise" or msg == "Clockwise":
        body = "clockwise"
        message = "Go Red Team! Arm 1 Rotating Clockwise!"
    elif msg == "COUNTERCLOCKWISE" or msg == "counterclockwise" or msg == "Counterclockwise" or msg == "Counter clockwise" or msg == "counter clockwise" or msg == "COUNTER CLOCKWISE" or msg == "Counter Clockwise":
        body = "counterclockwise"
        message = "Go Red Team! Arm 1 Rotating Counterclockwise!"
    elif msg == "CATCH" or msg == "catch" or msg == "Catch":
        body = "catch"
        message = "Go Red Team! Arm 1 Grabbing!"
    elif msg == "RELEASE" or msg == "release" or msg == "Release":
        body = "release"
        message = "Go Red Team! Arm 1 Dropping!"
    elif msg == "RESET" or msg == "reset" or msg == "Reset":
        body = "reset"
        message = "Reset!"
    else:
        message = "Sorry, that's not a valid command!"

    resp = twiml.Response()
    resp.message(message)
    print_to_console(body)
    #write_to_txt("Uarm1 : " + body + "\n")
    oscmsg = OSC.OSCMessage()
    oscmsg.setAddress("/uarm1")
    oscmsg.append(body)
    c.send(oscmsg)
    return str(resp)
    


@app.route("/arm2", methods=['GET', 'POST'])
def sms2():

    msg = request.form['Body']
    

    if msg == "UP" or msg == "up" or msg == "Up":
        message = "Go Blue Team! Arm 2 Moving Up!"
        body = "up"
    elif msg == "DOWN" or msg == "down" or msg == "Down":
        message = "Go Blue Team! Arm 2 Moving Down!"
        body = "down"
    elif msg == "LEFT" or msg == "left" or msg == "Left":
        message = "Go Blue Team! Arm 2 Moving Left!"
        body = "left"
    elif msg == "RIGHT" or msg == "right" or msg == "Right":
        message = "Go Blue Team! Arm 2 Moving Right!"
        body = "right"
    elif msg == "FORWARD" or msg == "forward" or msg == "Forward":
        message = "Go Blue Team! Arm 2 Moving Forward!"
        body = "forward"
    elif msg == "BACK" or msg == "back" or msg == "Back":
        message = "Go Blue Team! Arm 2 Moving Back!"
        body = "back"
    elif msg == "CLOCKWISE" or msg == "clockwise" or msg == "Clockwise":
        message = "Go Blue Team! Arm 2 Rotating Clockwise!"
        body = "clockwise"
    elif msg == "COUNTERCLOCKWISE" or msg == "counterclockwise" or msg == "Counterclockwise" or msg == "Counter clockwise" or msg == "counter clockwise" or msg == "COUNTER CLOCKWISE" or msg == "Counter Clockwise":
        message = "Go Blue Team! Arm 2 Rotating Counterclockwise!"
        body = "counterclockwise"
    elif msg == "CATCH" or msg == "catch" or msg == "Catch":
        message = "Go Blue Team! Arm 2 Grabbing!"
        body = "catch"
    elif msg == "RELEASE" or msg == "release" or msg == "Release":
        message = "Go Blue Team! Arm 2 Dropping!"
        body = "release"
    elif msg == "RESET" or msg == "reset" or msg == "Reset":
        message = "Reset!"
        body = "reset"
    else:
        message = "Sorry, that is not a valid command!"

    resp = twiml.Response()
    resp.message(message)    
    print_to_console(body)
    #write_to_txt("Uarm1 : " + body + "\n")
    oscmsg = OSC.OSCMessage()
    oscmsg.setAddress("/uarm2")
    oscmsg.append(body)
    #c.send(oscmsg)
    c2.send(oscmsg)
    return str(resp)



if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
    