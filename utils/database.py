from flask import Blueprint, request, jsonify
import json,requests
from utils.connect import client, db
from bson import ObjectId
from datetime import datetime
from bson.json_util import dumps


#todo

'''-----------------------------------
        saving to the database
-----------------------------------'''

# find the cctv collection with camera_id
#if not there, then create one
#if already exits then append the new person's details into the collection

'''
def save_frame(video_id,cctv_id,frame_output,timestamp):
    if video_id == None:
        status = False
        message = "No Object Id in param."
        return status,message
    else:
        if "cctv" not in db.list_collection_names():
            status = False
            message = "No Object Id in param."
            return status,message
        else:
            cctv = db.cctv.find_one({ "_id": ObjectId(video_id)})
            status = False
            message = "No Object Id in param."
            return status,message

'''


'''-----------------------------------
    narrowing down the database
-----------------------------------'''

#fetch all the data of the cctv collection
#compare the each frame with the next frame and remove duplicates
#identify the unique person in frames with the last seen timestamp
#save the details into a new collection

'''
def video_narrow(video_id,cctv_id,frame_output,timestamp):
    if video_id == None:
        status = False
        message = "No Object Id in param."
        return status,message
    else:
        if "cctv" not in db.list_collection_names():
            status = False
            message = "No Object Id in param."
            return status,message
        else:
            cctv = db.cctv.find_one({ "_id": ObjectId(video_id)})
            status = False
            message = "No Object Id in param."
            return status,message

'''