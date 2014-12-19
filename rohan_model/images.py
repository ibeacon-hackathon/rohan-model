#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the Rohan project of the 2014 iBeacon hackathon
# https://github.com/ibeacon-hackathon/

__author__="Alon Diamant"
__email__ = "diamant.alon@gmail.com"

'''
Users.
'''

import db
import logging
from functools import wraps

#=======================================================================================================================
# Public Interface
#=======================================================================================================================

def set(id, data):
    '''
    Sets an image.

    :param id:
    :param data:
    :return: True for success, False otherwise.
    '''

    try:

        db.images().child(id).put(data)

        return True
    except Exception as e:
        logging.exception("Couldn't create new image with id %s!" % id)
        return False

def get(id):
    '''
    Gets an image

    :param id:
    :return: dict or None
    '''

    try:
        return db.images().child(id).get()
    except Exception as e:
        logging.exception("Couldn't get user!")
        return None

#=======================================================================================================================
# Private Implementation
#=======================================================================================================================

#=======================================================================================================================
# Tests
#=======================================================================================================================

if __name__ == "__main__":

    print "Starting tests..."

    # Set an image
    imageContent = "imageimageimage"
    set("someImage", "imageimageimage")
    read = get("someImage")
    print read
    assert read == "imageimageimage"

    print "Done"