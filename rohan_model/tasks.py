#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the Rohan project of the 2014 iBeacon hackathon
# https://github.com/ibeacon-hackathon/

__author__="Alon Diamant"
__email__ = "diamant.alon@gmail.com"

'''
Tasks.
'''

import db
import logging
import datetime
import lists
import users
from users import verifyLogin
from gcm import GCM

#=======================================================================================================================
# Public Interface
#=======================================================================================================================

@verifyLogin
def get(id, accessToken=None):
    '''
    Returns a dict in the following format:


        id
        name (human readable)
        description (human readable)
        points (int)
        status (can be: "open", "accepted", "done", "verified)
        user (id of a user)
        list (id of a list)
        creationTime (datetime)
        acceptedtime (datetime)
        finishedTime (datetime)
        imageUrl

    :param id: task id
    :return: dict or None
    '''

    try:
        task = _get(id)

        if task:
            task["creationTime"] = datetime.datetime.strptime(task["creationTime"], "%Y-%m-%d %H:%M:%S.%f")
        return task
    except Exception as e:
        logging.exception("Couldn't get task!")
        return None

@verifyLogin
def new(id, name, description, points, listId, accessToken=None):
    '''
    Creates a new task with the parameters inputted.

    :param id:
    :param name: human readable
    :param description: human readable
    :param points: points to award winner
    :param listId: id of a list
    :return:
    '''

    try:

        if _get(id):
            logging.error("Task with id %s already exists!", id)
            return False

        if not lists.exists(listId, accessToken=accessToken):
            logging.error("List with id %s doesn't exist.", listId)
            return False

        task = {}
        task['id'] = id
        task['name'] = name
        task['description'] = description
        task['points'] = points
        task['status'] = "open"
        task['user'] = None
        task['list'] = listId
        task['creationTime'] = datetime.datetime.now().isoformat(' ')
        task['acceptedTime'] = None
        task['finishedTime'] = None
        task['imageUrl'] = None

        db.tasks().child(id).put(task)

        return lists.attachTask(listId, id, accessToken=accessToken)

    except Exception as e:
        logging.exception("Couldn't create new task with id %s!" % id)
        return False

@verifyLogin
def delete(id, accessToken=None):
    '''
    Delete a task.

    :param id:
    :return:
    '''

    try:

        task = _get(id)

        if not task:
            logging.error("Task with id %s doesn't exist!", id)
            return False

        # Delete from list too
        listId = task['list']

        lists.detachTask(listId, id, accessToken=accessToken)

        db.tasks().child(id).delete()

        return True
    except Exception as e:
        logging.exception("Couldn't delete task with id %s!" % id)
        return False

@verifyLogin
def accept(id, userId, accessToken=None):
    '''
    Accepts a task, settings the user's id to it's user field.

    :param id:
    :param userId:
    :return:
    '''

    try:

        task = _get(id)

        if not task:
            logging.error("Task with id %s doesn't exist!", id)
            return False

        if 'user' in task and task['user']:
            logging.error("Task already has user %s.", task['user'])
            return False

        if task['status'] != 'open':
            logging.error("Task with id %s has status %s (not 'open')" % (id, task['status']))
            return False

        if not lists.canAccess(task['list'], userId, accessToken=accessToken):
            logging.error("User %s can not access list %s.", userId, task['list'])

        task['status'] = "accepted"
        task['user'] = userId

        _update(id, task)

        return True

    except:
        logging.exception("Failed accepting task with id %s", id)
        return False

@verifyLogin
def finish(id, userId, imageUrl, accessToken=None):
    '''
    Marks a task as finished, verifying the reporting userId indeed has accepted it and setting an imageUrl if it
    exists.

    :param id:
    :param userId:
    :param imageUrl:
    :return:
    '''

    try:

        task = _get(id)

        if not task:
            logging.error("Task with id %s doesn't exist!", id)
            return False

        # After this, no need ot check access
        if task['user'] != userId:
            logging.error("Task with id %s has user %s (not %s)" % (id, task['user'], userId))
            return False

        if task['status'] != 'accepted':
            logging.error("Task with id %s has status %s (not 'accepted')" % (id, task['status']))
            return False

        task['status'] = "done"
        task['imageUrl'] = imageUrl


        # Update the task
        _update(id, task)

        # Send a PN
        data = {
            "type": "done",
            "task_id": task['id'],
            "task_name": task['name'],
            "image_url": imageUrl
        }

        # To all admins of the task
        mylist = lists.get(task['list'], accessToken=accessToken)
        for admin in mylist['admins']:
            user = users.get(admin, accessToken=accessToken)
            pushToken = user['pushToken']
            _sendPN(pushToken, data)

        return True

    except:
        logging.exception("Failed finishing task with id %s", id)
        return False

@verifyLogin
def cancel(id, userId, accessToken=None):
    '''
    Marks a task as cancelled, removing the user's marking as accepted.

    :param id:
    :param userId:
    :return:
    '''

    try:

        task = _get(id)

        if not task:
            logging.error("Task with id %s doesn't exist!", id)
            return False

        # After this, no need ot check access
        if task['user'] != userId:
            logging.error("Task with id %s has user %s (not %s)" % (id, task['user'], userId))
            return False

        if task['status'] != 'accepted':
            logging.error("Task with id %s has status %s (not 'accepted')" % (id, task['status']))
            return False

        task['status'] = "open"
        task['user'] = None

        _update(id, task)

        return True

    except:
        logging.exception("Failed finishing task with id %s", id)
        return False

@verifyLogin
def verify(id, accessToken=None):
    '''
    Marks a task as verified, awarding the points to the user..

    :param id:
    :return:
    '''

    try:

        task = _get(id)

        if not task:
            logging.error("Task with id %s doesn't exist!", id)
            return False

        if task['status'] != 'done':
            logging.error("Task with id %s has status %s (not 'done')" % (id, task['status']))
            return False

        # Hack - access token is equal to user name
        if not lists.isAdmin(task['list'], userId=accessToken, accessToken=accessToken):
            logging.error("User %s is not admin of list %s.", accessToken, task['list'])

        task['status'] = "verified"

        user = task['user']
        list = task['list']
        points = task['points']

        _update(id, task)

        lists.increaseScore(list, user, points, accessToken=accessToken)

        # Send a PN
        data = {
            "type": "verified",
            "task_id": task['id'],
            "task_name": task['name']
        }

        # To the user that finished the task
        user = users.get(user, accessToken=accessToken)
        pushToken = user['pushToken']
        _sendPN(pushToken, data)

        return True

    except:
        logging.exception("Failed finishing task with id %s", id)
        return False


#=======================================================================================================================
# Private Implementation
#=======================================================================================================================

def _get(id):

    return db.tasks().child(id).get()

def _update(id, task):

    try:

        task = db.tasks().child(str(id)).update(task)

        return True

    except:
        logging.exception("Failed updating task with id %s", id)
        return False

def _sendPN(deviceToken, data):

    gcmAPIKey = "GCMAPIKEY"

    gcm = GCM(gcmAPIKey)

    try:
        #deviceToken = "APA91bH0dZinGsSGWG5-hA0ZVMbmupjmY4MUcMqMVveBe9vmy2wjyLf7z_ndhOwSQSrMddW-mVa8ujOKnP9v5D4-j56ogjY_JUYmwnXP45pmmBIfljyRM5aj8GJFa06BEczNJl4Epdki19r2sFRxiIZExp_tre8l6A3RYb2KF7oS65kJi-qjlKA"

        payloadData = {
            "to" : deviceToken,
            "message_id": "reg_id",
            "data": data
        }

        print "Sending PN: %s" % data

        response = gcm.json_request(registration_ids=[deviceToken],
                                    data=payloadData)

        print response
    except:
        logging.exception("Failure sending push notification.")


#=======================================================================================================================
# Tests
#=======================================================================================================================

if __name__ == "__main__":

    print "Starting tests..."

    # Reset DB
    db.resetDB()

    accessToken = users.login("diamant.alon@gmail.com")

    # Get a task
    taskA = get("v3r1f13dt45k", accessToken=accessToken)
    print taskA
    assert taskA

    # Create a new task
    created = new("test", "Test task", "Perform a test task to completion!", 500, "3ntr4nc3", accessToken=accessToken)
    print created
    assert created

    created = new("test", "", "", 0, "", accessToken=accessToken)
    print created
    assert not created

    test = get("test", accessToken=accessToken)
    print test
    assert test

    deleted = delete("test", accessToken=accessToken)
    print deleted
    assert deleted

    mylist = lists.get("3ntr4nc3", accessToken=accessToken)
    oldScore = mylist['scores']['alon']

    # Create a new task
    created = new("test", "Test task", "Perform a test task to completion!", 500, "3ntr4nc3", accessToken=accessToken)
    print created
    assert created

    accepted = accept("test", "alon", accessToken=accessToken)
    print accepted
    assert accepted

    canceled = cancel("test", "alon", accessToken=accessToken)
    print canceled
    assert canceled

    accepted = accept("test", "alon", accessToken=accessToken)
    print accepted
    assert accepted

    done = finish("test", "alon", "http://www.image.com", accessToken=accessToken)
    print done
    assert done

    verified = verify("test", accessToken=accessToken)
    print verified
    assert verified

    # Check the score
    mylist = lists.get("3ntr4nc3", accessToken=accessToken)
    assert mylist['scores']['alon'] == oldScore + 500

    print "Done"
