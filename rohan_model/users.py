#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the Rohan project of the 2014 iBeacon hackathon
# https://github.com/ibeacon-hackathon/
from functools import wraps

__author__="Alon Diamant"
__email__ = "diamant.alon@gmail.com"

'''
Users.
'''

import db
import logging

#=======================================================================================================================
# Public Interface
#=======================================================================================================================

def register(id, firstName, lastName, email, pushToken):
    '''
    Creates a new user with the parameters inputted.

    :param id:
    :param firstName:
    :param lastName:
    :param pushToken:
    :param email:
    :return: True for success, False otherwise.
    '''

    try:
        if _get(id):
            logging.error("User with id %s already exists!", id)
            return False

        user = {}
        user['id'] = id
        user['lastName'] = lastName
        user['firstName'] = firstName
        user['email'] = email
        user['pushToken'] = pushToken

        db.users().child(id).put(user)

        db.emails_to_users().patch({_createEmailKey(email):id})
        return True
    except Exception as e:
        logging.exception("Couldn't create new user with id %s!" % id)
        return False

def login(email):
    '''
    Verify that an email address is of a user, and is allowed to access our database.
    :param email:
    :return: An access token to pass to other method if a user exists, or None
    '''

    # TODO: For this hackathon, we'll just verify the email, and if it exists - great.
    #       No real security here, and in fact - anyone can do anything.
    #       In the future, we can

    try:
        emailKey = _createEmailKey(email)

        id = db.emails_to_users().child(emailKey).get()
        user = _get(id)

        # TODO: Proper verification - now we just check the email is found
        if user:
            return _createAccessToken(user['id'])
        else:
            return None

    except Exception as e:
        logging.exception("Couldn't verify user with email %s!" % email)
        return None

def verifyLogin(f, *args, **kwargs):
    """
    Decorator that verifies an access token says the user is logged in.
    """
    def verifier(*args, **kwargs):
        if not 'accessToken' in kwargs:
            raise Exception("Missing access token!")
        else:
            if not _verify(accessToken=kwargs['accessToken']):
                print "Failed to verify loging for token %s." % kwargs['accessToken']
                raise Exception("Invalid access token!")
            else:
                print "Verified login for token %s." % kwargs['accessToken']
        return f(*args, **kwargs)
    return wraps(f)(verifier)

@verifyLogin
def get(id, accessToken=None):
    '''
    Returns a dict in the following format:

        id
        firstName
        lastName
        email
        pushToken

    :param id:
    :return: dict or None
    '''

    try:
        return _get(id)
    except Exception as e:
        logging.exception("Couldn't get user!")
        return None

@verifyLogin
def exists(id, accessToken=None):
    '''
    Checks whether a user id exists or not.
    :param id:
    :return: True or False.
    '''

    if _get(id):
        return True
    else:
        return False

@verifyLogin
def delete(id, accessToken=None):
    '''
    Delete a user.

    :param id:
    :return:
    '''

    try:
        user = _get(id)
        emailKey = _createEmailKey(user['email'])
        db.users().child(id).delete()
        db.emails_to_users().child(emailKey).delete()

        return True
    except Exception as e:
        logging.exception("Couldn't delete user with id %s!" % id)
        return False

#=======================================================================================================================
# Private Implementation
#=======================================================================================================================

def _createEmailKey(email):

    return email.replace(".", ",")

def _createAccessToken(userId):

    return userId

def _get(id):

    return db.users().child(id).get()

def _verify(accessToken):
    '''
    Verifies an access token.

    :param accessToken:
    :return: True or False.
    '''

    # TODO: The access token is just a user id, we see if it exists.. for now. Simple and crappy.
    if _get(accessToken):
        return True
    else:
        return False

#=======================================================================================================================
# Tests
#=======================================================================================================================

if __name__ == "__main__":

    print "Starting tests..."

    # Reset DB
    db.resetDB()

    accessToken = login("diamant.alon@gmail.com")

    # Get a user
    alon = get("alon", accessToken=accessToken)
    print alon
    assert alon

    if exists("test", accessToken=accessToken):
        delete("test", accessToken=accessToken)

    # Create a new user
    created = register("test", "test", "me", "test123@gmail.com", "pushToken")
    print created
    assert created

    exist = exists("test", accessToken=accessToken)
    print exist
    assert exist

    created = register("test", "test2", "me2", "test1232@gmail.com", "pushToken")
    print created
    assert not created

    test = get("test", accessToken=accessToken)
    print test
    assert test

    token = login("test123@gmail.com")
    print token
    assert token

    verified = exists("test", accessToken=token)
    print verified
    assert verified

    try:
        token = exists("test", accessToken="lalalacom")
    except:
        token = None
    print token
    assert not token

    try:
        verified = login("23123123")
    except:
        verified = None
    print verified
    assert not verified

    deleted = delete("test", accessToken=accessToken)
    print deleted
    assert deleted

    test = get("test", accessToken=accessToken)
    print test
    assert not test

    exist = exists("test", accessToken=accessToken)
    print exist
    assert not exist

    verified = login("test123@gmail.com")
    print verified
    assert not verified

    print "Done"