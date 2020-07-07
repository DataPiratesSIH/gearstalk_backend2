"""
Create multiple RabbitMQ connections from a single thread, using Pika and multiprocessing.Pool.
Based on tutorial 2 (http://www.rabbitmq.com/tutorials/tutorial-two-python.html).
"""

#concurrent_futures subprocessing
import concurrent.futures
import time
import json

import pika

executor = concurrent.futures.ProcessPoolExecutor(max_workers=5)

def callback(ch, method, properties, body):
    print(" [x] Received {}".format(json.loads(body)['frame_sec']))
    time.sleep(3)
    print(" [x] Done {}".format(json.loads(body)['frame_sec']))
    # ch.basic_ack(delivery_tag=method.delivery_tag)


def consume():
    credentials = pika.PlainCredentials('test', 'test')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=credentials))                       #load_balancer url/ip in (host)
    channel = connection.channel()

    channel.queue_declare(queue='video_frame')

    channel.basic_consume(
        queue='video_frame', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        pass



if __name__ == '__main__':
    # app.run(host="0.0.0.0", debug=True, use_reloader=True, threaded=True)
    try:
        while True:
            executor.submit(consume)
    except KeyboardInterrupt:
        while True:
            quit = True


# import concurrent.futures
# from concurrent.futures import ProcessPoolExecutor
# import urllib.request

# URLS = ['http://www.foxnews.com/',
#    'http://www.cnn.com/',
#    'http://europe.wsj.com/',
#    'http://www.foxnews.com/',
#    'http://www.cnn.com/',
#    'http://europe.wsj.com/',
#    'http://www.bbc.co.uk/',
#    'http://some-made-up-domain.com/']

# def load_url(url, timeout):
#     print(url)
#     time.sleep(2)
#     with urllib.request.urlopen(url, timeout = timeout) as conn:
#         return conn.read()

# def main():
#    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
#       future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
#       for future in concurrent.futures.as_completed(future_to_url):
#         url = future_to_url[future]
#         try:
#             data = future.result()
#         except Exception as exc:
#             print('%r generated an exception: %s' % (url, exc))
#         else:
#             print('%r page is %d bytes' % (url, len(data)))

# if __name__ == '__main__':
#    main()