import os
from flask import Flask, request, jsonify, make_response, render_template, Response
import json,requests
import time
import cv2
import numpy as np
from skimage import io
import datetime
from flask_pymongo import pymongo
import base64
import datetime



app = Flask(__name__)
CONNECTION_STRING = 'mongodb+srv://admin:admin@cluster0-jnsfh.mongodb.net/test?retryWrites=true&w=majority'
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('gearstalk')

#test to insert data to the data base
@app.route("/test")
def test():
    db.upload.insert_one({"name": "John"})
    return "Connected to the data base!"


#basic configurations
# derive the paths to the YOLO weights and model configuration
weightsPath = "./yolo_coco/yolov3.weights"
configPath = "./yolo_coco/yolov3.cfg"

#Load YOLO
net = cv2.dnn.readNet(weightsPath,configPath)
classes = []

# load the COCO class labels our YOLO model was trained on
labelsPath = "./yolo_coco/coco.names"
with open(labelsPath,"r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

'''-----------------------------------
            yolo-detection
-----------------------------------'''

def detect(img):
    img = cv2.resize(img,None,fx=1.0,fy=1.0)
    height,width,channels = img.shape

    #detecting objects
    blob = cv2.dnn.blobFromImage(img,0.00392,(416,416),(0,0,0),True,crop=False)   
    net.setInput(blob)
    outs = net.forward(outputlayers)

    #Showing info on screen/ get confidence score of algorithm in detecting an object in blob
    class_ids=[]
    confidences=[]
    boxes=[]
    l=[]                                                                                #for later use to list the confidences
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x= int(detection[0]*width)
                center_y= int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)
            
                #cv2.circle(img,(center_x,center_y),10,(0,255,0),2)
                #rectangle co-ordinaters
                x=int(center_x - w/2)
                y=int(center_y - h/2)
                #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                
                boxes.append([x,y,w,h])                                                     #put all rectangle areas
                confidences.append(float(confidence))                                       #how confidence was that object detected and show that percentage
                class_ids.append(class_id)                                                  #name of the object tha was detected

    indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.4,0.6)

    for i in range(len(boxes)):
        if i in indexes:
            x,y,w,h = boxes[i]
            name = str(classes[class_ids[i]])
            if name == 'person':
                crop_img = img[y:y+h, x:x+w+40]
                # features = df2.fashion(crop_img)
                # classify.fashion(crop_img)
                l.append('{}'.format(name))
    return l



@app.route('/')
def index():
    try:
        
        return '''
            <h1><b>Fashion App</b></h1>
        '''
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.get_json()
        string = data['img']
        filename = data['filename']

        original = base64.b64decode(string)
        np_image = np.frombuffer(original, dtype=np.uint8)
        img = cv2.imdecode(np_image, flags=1)

        print({'username' : sec,'profile_image_name' : filename})
        # db.save_file(profile_image.filename, profile_image)
        # db.upload.insert({'username' : request.form.get('username'),'profile_image_name' : profile_image.filename})

        return jsonify({'username' : data['sec'],'profile_image_name' : data['filename']}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/live', methods=['POST'])
def livestream():
    try:
        data = request.get_json()
        cam_id = data['cam_id']
        lat = data['lat']
        lng = data['lng']
        url = data['url']

        #image
        image = cv2.cvtColor(io.imread(url), cv2.COLOR_BGR2RGB)

        features = detect(image)

        #datetime
        currentDT = datetime.datetime.now()
        frame_time = currentDT.strftime("%I:%M:%S %p")
        frame_date = currentDT.strftime("%b %d, %Y")
        frame_day = currentDT.strftime("%a")

        mydata = {
            "cam_id" : cam_id,
            "lat" : lat,
            "lng" : lng,
            "features" : features,
            "date" : frame_date,
            "time" : frame_time,
            "day" : frame_day
        }

        db.live.insert(mydata)

        return jsonify(mydata), 200
    except Exception as e:
        return f"An Error Occured: {e}"



if __name__ == '__main__':
    app.run(host='127.0.1.1', port='8080', debug=True, use_reloader=True, threaded=True)