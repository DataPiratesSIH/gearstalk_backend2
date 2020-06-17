import os
from flask import Flask, request, jsonify, make_response, render_template, Response
from flask_cors import CORS
import json,requests
import time
import cv2
import numpy as np
from skimage import io
import datetime
from flask_pymongo import pymongo
import base64
import datetime
import utils.yolo as yolo
import utils.database as database



app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


'''************************************************
                    Routes
************************************************'''

'''
#test to insert data to the data base
@app.route("/test")
def test():
    db.upload.insert_one({"name": "John"})
    return "Connected to the data base!"
'''


@app.route('/')
def index():
    try:
        return '''
            <h1><b>GEARSTALK-BACKEND-2</b></h1>
        '''
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/FashionFrame', methods=['POST'])
def FashionFrame():
    try:
        start = time.time()
        data = request.form
        video_id = data['video_id']
        frame_sec = data['frame_sec']
        timestamp = data['timestamp']
        cctv_id = data['cctv_id']
        image = request.files['photo']
        image_cv = image.read()


        '''      convert the filestorge image to cv2 format       '''
        # (using file system instead)
        # original = base64.b64decode(string)                                                   # to convert the string image to image buffer

        np_image = np.frombuffer(image_cv, dtype=np.uint8)                                      # convert string data to numpy array
        
        img = cv2.imdecode(np_image, flags=1)                                                   # convert numpy array to image

        # print(img)
        # cv2.imshow('frame',img)
        # cv2.waitKey(0)
         
        print({
                "video_id": video_id,
                "frame_sec": frame_sec,
                "timestamp": timestamp,
                "cctv_id": cctv_id,
                "image": image.filename
            })

        
        '''      detection and classification       '''
        # start2 = time.time()
        frame_output = yolo.detect(img)
        # end = time.time()
        # print(frame_output)
        # print(end-start,end-start2)


        '''      writing into the database       '''
        # frame_output = [{"box": [41,71,11,30],"colors": ["#20211f","#565044"],"labels": ["Burkha"]}]


        start2 = time.time()
        status,message = database.save_frame(video_id,cctv_id,frame_output,timestamp,frame_sec)
        end = time.time()
        print(status,message)
        print(end-start,end-start2)


        return jsonify({"success": status, "message": message, "frame_output" : frame_output}), 200
    except Exception as e:
        return f"An Error Occured: {e}"



# @app.route('/live', methods=['POST'])
# def livestream():
#     try:
#         data = request.get_json()
#         cam_id = data['cam_id']
#         lat = data['lat']
#         lng = data['lng']
#         url = data['url']

#         #image
#         image = cv2.cvtColor(io.imread(url), cv2.COLOR_BGR2RGB)

#         features = detect(image)

#         #datetime
#         currentDT = datetime.datetime.now()
#         frame_time = currentDT.strftime("%I:%M:%S %p")
#         frame_date = currentDT.strftime("%b %d, %Y")
#         frame_day = currentDT.strftime("%a")

#         mydata = {
#             "cam_id" : cam_id,
#             "lat" : lat,
#             "lng" : lng,
#             "features" : features,
#             "date" : frame_date,
#             "time" : frame_time,
#             "day" : frame_day
#         }

#         db.live.insert(mydata)

#         return jsonify(mydata), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, threaded=True)