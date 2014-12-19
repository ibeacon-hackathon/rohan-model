#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the Rohan project of the 2014 iBeacon hackathon
# https://github.com/ibeacon-hackathon/

__author__="Alon Diamant"
__email__ = "diamant.alon@gmail.com"

'''
Lists.
'''

import logging
import db
import users
import tasks
from users import verifyLogin

#=======================================================================================================================
# Public Interface
#=======================================================================================================================

@verifyLogin
def get(id, accessToken=None):
    '''
    Returns a dict in the following format:

        id
        name (human readable)
        admins (array of user ids)
        users (array of user ids)
        public (boolean)
        scores (user ids to int)

    :param id: list id
    :return: dict or None
    '''

    try:
        return _get(id)
    except Exception as e:
        logging.exception("Couldn't get list!")
        return None

@verifyLogin
def new(id, name, adminIds, userIds, public, accessToken=None):
    '''
    Creates a new list with the parameters inputted.

    :param id:
    :param name:
    :param admins: list
    :param users: list
    :param public: bool
    :return: True for success, False otherwise.
    '''

    try:

        if _get(id):
            logging.error("List with id %s already exists!", id)
            return False

        mylist = {}
        mylist['id'] = id
        mylist['name'] = name

        for admin in adminIds:
            if not users.exists(admin, accessToken=accessToken):
                logging.error("Admin %s doesn't exist!", admin)
        mylist['admins'] = adminIds or []
        for user in userIds:
            if not users.exists(user, accessToken=accessToken):
                logging.error("User %s doesn't exist!", user)
        mylist['users'] = userIds or []
        mylist['scores'] = {}
        mylist['public'] = public
        mylist['tasks'] = {}

        db.lists().child(id).put(mylist)

        return True
    except Exception as e:
        logging.exception("Couldn't create new list with id %s!" % id)
        return False

@verifyLogin
def delete(id, accessToken=None):
    '''
    Delete a list.

    :param id:
    :return:
    '''

    try:

        mylist = _get(id)

        if not mylist:
            logging.error("List %s doesn't exist.", id)
            return False

        print mylist

        if 'tasks' in mylist:
            for task in mylist['tasks']:
                tasks.delete(task, accessToken=accessToken)

        db.lists().child(id).delete()

        return True

    except Exception as e:
        logging.exception("Couldn't delete list with id %s!" % id)
        return False


@verifyLogin
def exists(id, accessToken=None):
    '''
    Checks whether a task id exists or not.
    :param id:
    :return: True or False.
    '''

    if _get(id):
        return True
    else:
        return False

@verifyLogin
def attachTask(id, newTaskId, accessToken=None):
    '''
    This adds a task ID to the tasks array. It doesn't create a new task.

    :param id:
    :param newTaskId:
    :param accessToken:
    :return:
    '''

    mylist = _get(id)

    if not mylist:
        logging.error("List with id %s doesn't exist!", id)
        return False

    tasks = mylist['tasks'] or []
    tasks = set(tasks)
    tasks.add(newTaskId)
    mylist['tasks'] = list(tasks)

    print "tasks: %s" % str(mylist)

    return _update(id, mylist)

@verifyLogin
def detachTask(id, newTaskId, accessToken=None):
    '''
    This deletes a task ID from the tasks array. It doesn't create a new task.

    :param id:
    :param newTaskId:
    :param accessToken:
    :return:
    '''

    mylist = _get(id)

    if not mylist:
        logging.error("List with id %s doesn't exist!", id)
        return False

    tasks = mylist['tasks'] or []
    tasks = set(tasks)
    tasks.remove(newTaskId)
    mylist['tasks'] = list(tasks)

    return _update(id, mylist)

@verifyLogin
def attachAdmin(id, userId, accessToken=None):
    '''
    This adds a user ID to the admins array. It doesn't create a new user.

    :param id:
    :param userId:
    :param accessToken:
    :return:
    '''

    mylist = _get(id)

    if not mylist:
        logging.error("List with id %s doesn't exist!", id)
        return False

    admins = mylist['admins'] or []
    admins = set(admins)
    admins.add(userId)
    mylist['admins'] = list(admins)

    print "admins: %s" % str(mylist)

    return _update(id, mylist)

@verifyLogin
def detachAdmin(id, userId, accessToken=None):
    '''
    This deletes a user ID from the admins array. It doesn't create a new user.
    :param id:
    :param userId:
    :param accessToken:
    :return:
    '''

    mylist = _get(id)

    if not mylist:
        logging.error("List with id %s doesn't exist!", id)
        return False

    admins = mylist['admins'] or []
    admins = set(admins)
    admins.remove(userId)
    mylist['admins'] = list(admins)

    return _update(id, mylist)

@verifyLogin
def isAdmin(id, userId, accessToken=None):

    mylist = _get(id)

    if not mylist:
        logging.error("List with id %s doesn't exist!", id)
        return False

    admins = mylist['admins'] or []
    admins = set(admins)

    return userId in admins

@verifyLogin
def attachUser(id, userId, accessToken=None):
    '''
    This adds a user ID to the users array. It doesn't create a new user.
    :param id:
    :param userId:
    :param accessToken:
    :return:
    '''
    mylist = _get(id)

    if not list:
        logging.error("List with id %s doesn't exist!", id)
        return False

    users = mylist['users'] or []
    users = set(users)
    users.add(userId)
    mylist['users'] = list(users)

    return _update(id, mylist)

@verifyLogin
def detachUser(id, userId, accessToken=None):
    '''
    This deletes a user ID from the users array. It doesn't create a new user.
    :param id:
    :param userId:
    :param accessToken:
    :return:
    '''

    mylist = _get(id)

    if not list:
        logging.error("List with id %s doesn't exist!", id)
        return False

    users = mylist['users'] or []
    users = set(users)
    users.remove(userId)
    mylist['users'] = list(users)

    return _update(id, mylist)

@verifyLogin
def isUser(id, userId, accessToken=None):

    mylist = _get(id)

    if not mylist:
        logging.error("List with id %s doesn't exist!", id)
        return False

    users = mylist['users'] or []
    users = set(users)
    return userId in users

@verifyLogin
def setPublic(id, isPublic, accessToken=None):

    mylist = _get(id)

    if not mylist:
        logging.error("List with id %s doesn't exist!", id)
        return False

    mylist['public'] = isPublic

    return _update(id, mylist)

@verifyLogin
def isPublic(id, accessToken=None):

    mylist = _get(id)

    if not mylist:
        logging.error("List with id %s doesn't exist!", id)
        return False

    return mylist['public']

@verifyLogin
def canAccess(id, userId, accessToken=None):

    mylist = _get(id)

    if not mylist:
        logging.error("List with id %s doesn't exist!", id)
        return False

    return mylist['public'] or isAdmin(id, userId, accessToken=accessToken) or isUser(id, userId, accessToken=accessToken)

@verifyLogin
def increaseScore(id, userId, score, accessToken=None):
    '''
    Increase a score for a user in the context of the list.
    This shouldn't be called directly - instead, via the tasks module.

    :param id:
    :param userId:
    :param score:
    :param accessToken:
    :return:
    '''

    mylist = _get(id)

    if not list:
        logging.error("List with id %s doesn't exist!", id)
        return False

    if not 'scores' in mylist:
        mylist['scores'] = {}

    mylist['scores'][userId] = mylist['scores'].get(userId, 0) + score

    return _update(id, mylist)

#=======================================================================================================================
# Private Implementation
#=======================================================================================================================

def _get(id):

    return db.lists().child(id).get()

def _update(id, mylist):

    try:

        db.lists().child(id).update(mylist)
        return True

    except:
        logging.exception("Failed updating task with id %s", id)
        return False

#=======================================================================================================================
# Tests
#=======================================================================================================================

if __name__ == "__main__":

    print "Starting tests..."

    # Reset DB
    db.resetDB()

    accessToken = users.login("diamant.alon@gmail.com")

    # Get a list
    listA = get("3ntr4nc3", accessToken=accessToken)
    print listA
    assert listA

    # Just in case
    deleted = delete("test", accessToken=accessToken)

    # Create a new list
    created = new("test", "Test list", ["alon", "avi"], ["joshua", "erez"], False, accessToken=accessToken)
    print created
    assert created

    created = new("test", "Empty shit", [], [], False, accessToken=accessToken)
    print created
    assert not created

    test = get("test", accessToken=accessToken)
    print test
    assert test

    deleted = delete("test", accessToken=accessToken)
    print deleted
    assert deleted

    admin = isAdmin("b4ck3ndT4bl3", "alon", accessToken=accessToken)
    print admin
    assert admin

    admin = isAdmin("b4ck3ndT4bl3", "joshua", accessToken=accessToken)
    print admin
    assert not admin

    admin = attachAdmin("b4ck3ndT4bl3", "joshua", accessToken=accessToken)
    print admin
    assert admin

    admin = isAdmin("b4ck3ndT4bl3", "joshua", accessToken=accessToken)
    print admin
    assert admin

    admin = detachAdmin("b4ck3ndT4bl3", "joshua", accessToken=accessToken)
    print admin
    assert admin

    admin = isAdmin("b4ck3ndT4bl3", "joshua", accessToken=accessToken)
    print admin
    assert not admin

    user = isUser("fr0nt3ndT4ble", "avi", accessToken=accessToken)
    print user
    assert user

    user = isUser("fr0nt3ndT4ble", "joshua", accessToken=accessToken)
    print user
    assert not user

    user = attachUser("fr0nt3ndT4ble", "joshua", accessToken=accessToken)
    print user
    assert user

    user = isUser("fr0nt3ndT4ble", "joshua", accessToken=accessToken)
    print user
    assert user

    user = detachUser("fr0nt3ndT4ble", "joshua", accessToken=accessToken)
    print user
    assert user

    user = isUser("fr0nt3ndT4ble", "joshua", accessToken=accessToken)
    print user
    assert not user

    public = isPublic("fr0nt3ndT4ble", accessToken=accessToken)
    print public
    assert not public

    public = setPublic("fr0nt3ndT4ble", True, accessToken=accessToken)
    print public
    assert public

    public = isPublic("fr0nt3ndT4ble", accessToken=accessToken)
    print public
    assert public

    public = setPublic("fr0nt3ndT4ble", False, accessToken=accessToken)
    print public
    assert public

    public = isPublic("fr0nt3ndT4ble", accessToken=accessToken)
    print public
    assert not public

    access = canAccess("fr0nt3ndT4ble", "joshua", accessToken=accessToken)
    print access
    assert not access

    public = setPublic("fr0nt3ndT4ble", True, accessToken=accessToken)
    print public
    assert public

    access = canAccess("fr0nt3ndT4ble", "joshua", accessToken=accessToken)
    print access
    assert access

    public = setPublic("fr0nt3ndT4ble", False, accessToken=accessToken)
    print public
    assert public

    access = canAccess("fr0nt3ndT4ble", "joshua", accessToken=accessToken)
    print access
    assert not access

    user = attachUser("fr0nt3ndT4ble", "joshua", accessToken=accessToken)
    print user
    assert user

    access = canAccess("fr0nt3ndT4ble", "joshua", accessToken=accessToken)
    print access
    assert access

    user = detachUser("fr0nt3ndT4ble", "joshua", accessToken=accessToken)
    print user
    assert user

    access = canAccess("fr0nt3ndT4ble", "joshua", accessToken=accessToken)
    print access
    assert not access

    mylist = get("fr0nt3ndT4ble", accessToken=accessToken)
    oldScore = mylist['scores'].get('alon', 0)

    increaseScore("fr0nt3ndT4ble", "alon", 100, accessToken=accessToken)
    mylist = get("fr0nt3ndT4ble", accessToken=accessToken)
    newScore = mylist['scores'].get('alon', 0)
    assert oldScore + 100 == newScore

    print "Done"