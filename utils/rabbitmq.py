import pika
import json
import os

from app import FashionFrame
from dotenv import load_dotenv

load_dotenv()
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")



'''-----------------------------------------
        Consuming packets from rabbitmq
        and adding it into a subprocess
------------------------------------------'''

def rabbitmq_consumer():
    credentials = pika.PlainCredentials('gearstalk', 'gearstalk')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='139.59.12.237',port=5672,credentials=credentials))                       #load_balancer url/ip in (host)
    channel = connection.channel()
    

    channel.queue_declare(queue='video_frame')

    def callback(ch, method, properties, body):
            print(" [x] Received ")
            FashionFrame(body)


    channel.basic_consume(
        queue='video_frame', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()



'''-----------------------------------------
        Producing packets into rabbitmq
                after processing
------------------------------------------'''

def rabbitmq_producer(data):
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST,port=5672,
                                    credentials=credentials))                       #load_balancer url/ip in (host)
    channel = connection.channel()

    channel.queue_declare(queue='frame_output')

    message = json.dumps(data)
    
    channel.basic_publish(exchange='', routing_key='frame_output', body=message)
    print(" [x] Sent The JSON Data")
    connection.close()




'''-----------------------------------------
        Producing failed packets into
                rabbitmq queue
------------------------------------------'''

def rabbitmq_reproducer(data):
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST,port=5672,
                                    credentials=credentials))                       #load_balancer url/ip in (host)
    channel = connection.channel()

    channel.queue_declare(queue='video_frame')

    message = json.dumps(data)
    
    channel.basic_publish(exchange='', routing_key='video_frame', body=message)
    print(" [x] ReSent The JSON Data into the queue")
    connection.close()



'''-----------------------------------------
        For Realtime Detection (todo)
------------------------------------------'''

'''
def rabbitmq_live(cam_id, lat, lng, url):
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='127.0.1.1', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='live_data')

    data = {
        "cam_id" : str(cam_id),
        "lat" : lat,
        "lng" : lng,
        "url" : url
    }
    message = json.dumps(data, ensure_ascii=False, indent=4)
    print(message)

    channel.basic_publish(exchange='', routing_key='live_data', body=message)
    print(" [x] Sent The JSON Data")
    connection.close()

'''