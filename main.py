from twilio.rest import Client
import course as c
from compassMethods import *
import os
import requests

def addMessages(messages):
    desiredClasses = []
    for message in messages:
        courseArr = message.body.split(" ")
        if len(courseArr) == 3 and len(courseArr[0]) == 4 and len(courseArr[1]) == 3 and len(courseArr[2]) == 3:
            if courseArr[0].isalpha() and courseArr[1].isnumeric() and courseArr[2].isnumeric():
                desiredClass = c.course(courseArr[0], int(courseArr[1]), int(courseArr[2]))
                desiredClasses.append(desiredClass)
    return desiredClasses

def findDeleteClassInMessage(messages):
    courses = []
    for message in messages:
        courseArr = message.body.split(" ")
        if courseArr[0] == "Remove":
            course = str(courseArr[1])+" "+str(courseArr[2])+" "+str(courseArr[3])
            courses.append(course)
    return courses



def deleteMessage(messages, course):
    for message in messages:
        if course in message.body:
            client.messages(message.sid).delete()

accountSID = os.environ["accountSID"]
auth_token = os.environ["auth_token"]
joshuapn = os.environ["joshuapn"]
seungjehpn = os.environ["seungjehpn"]

client = Client(accountSID, auth_token)
pn = [joshuapn, seungjehpn,]
for num in pn:
    messages = client.messages.list(from_= num, limit=200)

    deletedClass = findDeleteClassInMessage(messages)
    if len(deletedClass) != 0:
        for course in deletedClass:
            deleteMessage(messages, course)
            client.messages.create(to=num,
                                   from_="+13343104801",
                                   body="No longer searching for " + deletedClass)

    desiredClasses = addMessages(messages)
    notifiedClasses = []

    for mess in desiredClasses:
        if search(mess.dept, mess.num, mess.section):
            notifiedClasses.append(mess.printName())

    if len(notifiedClasses) != 0:
        body = ""
        for course in notifiedClasses:
            body += "\n"+course
        client.messages.create(to=num,
                               from_="+13343104801",
                               body="These Classes are open for registration: "+body)

