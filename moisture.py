import RPi.GPIO as GPIO
import smtplib # This is the SMTP library we need to send the email notification
import time # This is the time library, we need this so we can use the sleep function

smtp_username = "953f5757255401" # This is the username used to login to your SMTP provider
smtp_password = "f2fa4cc094bdd0" # This is the password used to login to your SMTP provider
smtp_host = "smtp.mailtrap.io" # This is the host of the SMTP provider
smtp_port = 25 # This is the port that your SMTP provider uses

smtp_sender = "from@smtp.mailtrap.io" # This is the FROM email address
smtp_receivers = "sandeshdawani4@gmail.com" # This is the TO email address

# This is the message that will be sent when NO moisture is detected

message_dead = """
Subject: Moisture Sensor Notification

Warning, no moisture detected!
"""

# This is the message that will be sent when moisture IS detected again

message_alive = """
Subject: Moisture Sensor Notification

Panic over! Water found again!
"""


def sendEmail(smtp_message):
    try:
        
        smtpObj = smtplib.SMTP(smtp_host, smtp_port)
        smtpObj.login(smtp_username, smtp_password) 
        smtpObj.sendmail(smtp_sender, smtp_receivers, smtp_message)         
        print ("Email has been sent")
    except smtplib.SMTPException:
        print ("Failed to send email")

# This function will be called every time there is a change on the specified GPIO channel, in this example we are using 17

def callback(channel):  
    if GPIO.input(channel):
        print ("No moisture detected")
        sendEmail(message_dead)
    else:
        print ("moisture detected")
        sendEmail(message_alive)

# Set our GPIO numbering to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin that we have our digital output from our sensor connected to
channel = 17

# Set the GPIO pin to an input
GPIO.setup(channel, GPIO.IN)

# This line tells our script to keep an eye on our gpio pin and let us know when the pin goes HIGH or LOW
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)

# This line asigns a function to the GPIO pin so that when the above line tells us there is a change on the pin, run this function
GPIO.add_event_callback(channel, callback)

# This is an infinte loop to keep our script running
while True:
    time.sleep(0.1) # wait of 0.1 second
