import pika
from lab_3_files import homework, json_writer
from tinydb import TinyDB
from threading import Lock, Thread
import argparse
import json


db = TinyDB('info.json')
db.truncate()
db_lock = Lock()


def work(threads):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    print(f' [{threads}] Rabbit has started and waiting for tasks.')

    def callback(ch, method, properties, body):
        print(f" [{threads}] Received link {body}.")
        result = homework.extract_info_from_page(body)

        with db_lock:
            db.insert(result)

        print(f" [{threads}] Successfully completed link {body}.")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    try:
        while True:
            method_frame, _, body = channel.basic_get(queue='task_queue')

            if body is None:
                print(f" [{threads}] Rabbit finished!")
                break

            callback(channel, method_frame, None, body)
    finally:
        connection.close()


def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Start the worker threads.")
    parser.add_argument('-t', '--threads', type=int, default=3, help='Number of threads to run')

    # Parse the command line arguments
    args = parser.parse_args()

    # Use the number of threads from the command line argument
    n_threads = args.threads

    threads = []
    for i in range(n_threads):
        t = Thread(target=work, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("_____PROCESSING FINISHED_____")


if __name__ == "__main__":
    main()

    # Beautify output file
    with open('info.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    json_writer.write(data, 'info.json')






