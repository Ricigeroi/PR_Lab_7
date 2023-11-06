from lab_3_files import in_class, json_writer
import pika
import argparse

url = "https://999.md/ro/list/real-estate/apartments-and-rooms"

# Set up the argument parser
parser = argparse.ArgumentParser(description="Extract links from website and send them to workers.")
parser.add_argument('-n', '--max_pages', type=int, default=1, help='Number of pages to process')

# Parse the command line arguments
args = parser.parse_args()

# Use the number of threads from the command line argument
max_page_num = args.max_pages


links = in_class.parse(url, max_page_num)
json_writer.write(links, "links.json")

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

for link in links:
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=link,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))

connection.close()
