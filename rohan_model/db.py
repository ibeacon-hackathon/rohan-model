#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the Rohan project of the 2014 iBeacon hackathon
# https://github.com/ibeacon-hackathon/
import json

__author__="Alon Diamant"
__email__ = "diamant.alon@gmail.com"

'''
Database stuff.

Using Firebase. Make sure to set the authorization stuff to set the "Security & Rules" to:
{
    "rules": {
        ".write": false,
        ".read": false
    }
}

Conclusion: Firebase is slow and doesn't make sense as a backend db. :)
'''

from firebase import Firebase

#=======================================================================================================================
# Public Interface
#=======================================================================================================================

def setup(baseUrl = 'https://rohan-db.firebaseio.com/', secret = None):
    global _baseUrl, _secret
    _baseUrl = baseUrl
    _secret = secret

def resetDB():
    testDB = json.loads(testDBString)
    users().put(testDB['users'])
    lists().put(testDB['lists'])
    emails_to_users().put(testDB['emails_to_users'])
    tasks().put(testDB['tasks'])
    images().put(testDB['images'])

def users():

    return _get().child("/users")

def lists():

    return _get().child("/lists")

def emails_to_users():

    return _get().child("/emails_to_users")

def tasks():

    return _get().child("/tasks")

def images():

    return _get().child("/images")

#=======================================================================================================================
# Private Implementation
#=======================================================================================================================

_baseUrl = 'https://rohan-db.firebaseio.com/'
_secret = None
_db = None

def _get():

    global _db, _secret

    if not _db:

        if not _secret:

            # Make sure secret.txt has your secret inside of it.
            with open("secret.txt") as f:

                _secret = f.readline().strip()

        _db = Firebase(_baseUrl, auth_token=_secret)

    return _db

testDBString = """
{
    "images" : {

    },
    "emails_to_users": {
        "diamant,alon@gmail,com": "alon",
        "jskrzypek@yoobic,com": "joshua",
        "werner,avi81@gmail,com": "avi",
        "gmistick@gmail,com": "yechiel",
        "refaelozeri@gmail,com": "refael",
        "erez@erezhod,com": "erez"
    },
    "users": {
        "alon": {
            "id": "alon",
            "firstName": "Alon",
            "lastName": "Diamant",
            "email": "diamant.alon@gmail.com",
            "pushToken": "APA91bH0dZinGsSGWG5-hA0ZVMbmupjmY4MUcMqMVveBe9vmy2wjyLf7z_ndhOwSQSrMddW-mVa8ujOKnP9v5D4-j56ogjY_JUYmwnXP45pmmBIfljyRM5aj8GJFa06BEczNJl4Epdki19r2sFRxiIZExp_tre8l6A3RYb2KF7oS65kJi-qjlKA"
        },
        "joshua": {
            "id": "joshua",
            "firstName": "Joshua",
            "lastName": "Skrzypek",
            "email": "jskrzypek@yoobic.com",
            "pushToken": "APA91bH0dZinGsSGWG5-hA0ZVMbmupjmY4MUcMqMVveBe9vmy2wjyLf7z_ndhOwSQSrMddW-mVa8ujOKnP9v5D4-j56ogjY_JUYmwnXP45pmmBIfljyRM5aj8GJFa06BEczNJl4Epdki19r2sFRxiIZExp_tre8l6A3RYb2KF7oS65kJi-qjlKA"
        },
        "avi": {
            "id": "avi",
            "firstName": "Avi",
            "lastName": "Werner",
            "email": "werner.avi81@gmail.com",
            "pushToken": "APA91bH0dZinGsSGWG5-hA0ZVMbmupjmY4MUcMqMVveBe9vmy2wjyLf7z_ndhOwSQSrMddW-mVa8ujOKnP9v5D4-j56ogjY_JUYmwnXP45pmmBIfljyRM5aj8GJFa06BEczNJl4Epdki19r2sFRxiIZExp_tre8l6A3RYb2KF7oS65kJi-qjlKA"
        },
        "yechiel": {
            "id": "yechiel",
            "firstName": "Yechiel",
            "lastName": "Levi",
            "email": "gmistick@gmail.com",
            "pushToken": "APA91bH0dZinGsSGWG5-hA0ZVMbmupjmY4MUcMqMVveBe9vmy2wjyLf7z_ndhOwSQSrMddW-mVa8ujOKnP9v5D4-j56ogjY_JUYmwnXP45pmmBIfljyRM5aj8GJFa06BEczNJl4Epdki19r2sFRxiIZExp_tre8l6A3RYb2KF7oS65kJi-qjlKA"
        },
        "refael": {
            "id": "refael",
            "firstName": "Refael",
            "lastName": "Ozeri",
            "email": "refaelozeri@gmail.com",
            "pushToken": "APA91bH0dZinGsSGWG5-hA0ZVMbmupjmY4MUcMqMVveBe9vmy2wjyLf7z_ndhOwSQSrMddW-mVa8ujOKnP9v5D4-j56ogjY_JUYmwnXP45pmmBIfljyRM5aj8GJFa06BEczNJl4Epdki19r2sFRxiIZExp_tre8l6A3RYb2KF7oS65kJi-qjlKA"
        },
        "erez": {
            "id": "erez",
            "firstName": "Erez",
            "lastName": "Hod",
            "email": "erez@erezhod.com",
            "pushToken": "APA91bH0dZinGsSGWG5-hA0ZVMbmupjmY4MUcMqMVveBe9vmy2wjyLf7z_ndhOwSQSrMddW-mVa8ujOKnP9v5D4-j56ogjY_JUYmwnXP45pmmBIfljyRM5aj8GJFa06BEczNJl4Epdki19r2sFRxiIZExp_tre8l6A3RYb2KF7oS65kJi-qjlKA"
        }
    },
    "lists": {
        "FC4695811A59" : {
            "id": "FC4695811A59",
            "name": "Our Beacon",
            "admins": [
                "alon",
                "yechiel"
            ],
            "users": [
                "avi",
                "joshua",
                "refael",
                "erez"
            ],
            "public": false,
            "scores": {
            },
            "tasks" : [
                "androidApp", "dbtask", "restfulApi", "pushNotificationSender"
            ]
        },
        "b4ck3ndT4bl3": {
            "id": "b4ck3ndT4bl3",
            "name": "Backend Table",
            "admins": [
                "alon",
                "avi"
            ],
            "users": [
                "yechiel"
            ],
            "public": false,
            "scores": {
                "alon": 1500,
                "joshua": 1900,
                "avi": 10000
            },
            "tasks" : [
                "s0m3t4sk", "4cc3pt3dT4sk"
            ]
        },
        "fr0nt3ndT4ble": {
            "id": "fr0nt3ndT4ble",
            "name": "Frontend Table",
            "admins": [
                "yechiel",
                "refael",
                "erez"
            ],
            "users": [
                "avi"
            ],
            "public": false,
            "scores": {
                "refael": 1800,
                "yechiel": 14000,
                "erez": 10000
            },
            "tasks" : [
                "07h3rT4sk"
            ]
        },
        "3ntr4nc3": {
            "id": "3ntr4nc3",
            "name": "Entrance",
            "admins": [
                "alon",
                "yechiel"
            ],
            "users": null,
            "public": true,
            "scores": {
                "alon": 1500,
                "joshua": 0,
                "avi": 0,
                "refael": 0,
                "yechiel": 0,
                "erez": 0
            },
            "tasks" : [
                "publ1cT45k", "pr3v10usly4cc3pt3dT4sk", "f1n1sh3dT4sk", "v3r1f13dt45k"
            ]
        }
    },
    "tasks": {
        "dbtask": {
            "id": "dbtask",
            "name": "Create the database",
            "description": "We really need it",
            "points": 300,
            "status": "open",
            "list": "FC4695811A59",
            "creationTime": "2014-12-18 11:58:43.000"
        },
        "androidApp": {
            "id": "androidApp",
            "name": "Create the Android app",
            "description": "It really is important",
            "points": 600,
            "status": "open",
            "list": "FC4695811A59",
            "creationTime": "2014-12-18 14:58:43.000"
        },
        "restfulApi": {
            "id": "restfulApi",
            "name": "Create the RESTful API",
            "description": "Without it we are nothing",
            "points": 50,
            "status": "open",
            "list": "FC4695811A59",
            "creationTime": "2014-12-18 19:58:43.000"
        },
        "pushNotificationSender": {
            "id": "pushNotificationSender",
            "name": "Create the Push Notificaiton sender",
            "description": "To let the users know what is up",
            "points": 100,
            "status": "open",
            "list": "FC4695811A59",
            "creationTime": "2014-12-18 21:58:43.000"
        },
        "s0m3t4sk": {
            "id": "s0m3t4sk",
            "name": "Create the database",
            "description": "We really need it",
            "points": 600,
            "status": "open",
            "list": "b4ck3ndT4bl3",
            "creationTime": "2014-12-18 21:58:43.000"
        },
        "07h3rT4sk": {
            "id": "07h3rT4sk",
            "name": "Create the Android app",
            "description": "We need to show something!",
            "points": 300,
            "status": "open",
            "list": "fr0nt3ndT4ble",
            "creationTime": "2014-12-18 21:59:14.000"
        },
        "publ1cT45k": {
            "id": "publ1cT45k",
            "name": "Close the door",
            "description": "It is really cold",
            "points": 1000,
            "status": "open",
            "list": "3ntr4nc3",
            "creationTime": "2014-12-18 21:59:33.000"
        },
        "4cc3pt3dT4sk": {
            "id": "4cc3pt3dT4sk",
            "name": "Create the RESTful API",
            "description": "Otherwise we can't connect anything to anything",
            "points": 200,
            "status": "accepted",
            "user": "alon",
            "list": "b4ck3ndT4bl3",
            "creationTime": "2014-12-18 21:58:43.000",
            "acceptedTime": "2014-12-18 22:08:43.000"
        },
        "pr3v10usly4cc3pt3dT4sk": {
            "id": "pr3v10usly4cc3pt3dT4sk",
            "name": "Create a $1 billion startup",
            "description": "So the VCs get their money back",
            "points": 500,
            "status": "open",
            "user": null,
            "list": "3ntr4nc3",
            "creationTime": "2014-12-18 22:04:43.000",
            "acceptedTime": null
        },
        "f1n1sh3dT4sk": {
            "id": "f1n1sh3dT4sk",
            "name": "Go home",
            "description": "We so tired",
            "points": 500,
            "status": "done",
            "user": "yechiel",
            "list": "3ntr4nc3",
            "creationTime": "2014-12-18 22:04:43.000",
            "acceptedTime": "2014-12-18 22:28:43.000",
            "finishedTime": "2014-12-18 23:08:43.000",
            "imageUrl": "http://www.xqa.com.ar/visualmanagement/wp-content/uploads/done_tag.jpg"
        },
        "v3r1f13dt45k": {
            "id": "v3r1f13dt45k",
            "name": "You really did it!",
            "description": "We so tired",
            "points": 500,
            "status": "verified",
            "user": "joshua",
            "list": "3ntr4nc3",
            "creationTime": "2014-12-18 22:04:43.000",
            "acceptedTime": "2014-12-18 22:28:43.000",
            "finishedTime": "2014-12-18 23:08:43.000",
            "imageUrl": "http://timemanagementninja.com/wp-content/uploads/2011/12/Finished.jpg"
        }
    }
}
"""

#=======================================================================================================================
# Tests
#=======================================================================================================================


if __name__ == "__main__":

    print "Starting tests..."

    resetDB()

    users = users().get()
    print users
    assert users

    lists = lists().get()
    print lists
    assert lists

    tasks = tasks().get()
    print tasks
    assert tasks

    emails_to_users = emails_to_users().get()
    print emails_to_users
    assert emails_to_users

    print "Done"