# PR_Lab_7 Repository

Welcome to the PR_Lab_7 repository! This repository contains a collection of Python scripts designed to interact with web pages, extract information, and work with RabbitMQ for message queuing.

## Repository Structure

The repository consists of the following Python scripts:

1. [homework.py](https://github.com/Ricigeroi/PR_Lab_7/blob/master/lab_3_files/homework.py): This script contains functions to extract information from a list of URLs using `requests` and `BeautifulSoup`. It processes each link, extracts specific details from the web pages, and returns the results in a structured format.

2. [in_class.py](https://github.com/Ricigeroi/PR_Lab_7/blob/master/lab_3_files/in_class.py): This script is used for parsing a given website link and recursively navigating through pages using `requests` and `BeautifulSoup`. It collects links from the pages up to a specified maximum page number.

3. [json_writer.py](https://github.com/Ricigeroi/PR_Lab_7/blob/master/lab_3_files/json_writer.py): A utility script to write Python dictionaries into JSON files with proper formatting and encoding.

4. [rabbits.py](https://github.com/Ricigeroi/PR_Lab_7/blob/master/rabbits.py): This script sets up RabbitMQ consumers (workers) that listen to a queue for tasks. It uses the `pika` library for RabbitMQ communication and `TinyDB` for storing the processed information.

5. [task_producer.py](https://github.com/Ricigeroi/PR_Lab_7/blob/master/task_producer.py): It acts as a producer that sends tasks to the RabbitMQ queue. It uses the `in_class.py` script to parse links from a website and then queues them for processing by workers.

## Getting Started

To use the scripts in this repository, you will need to have Python installed on your system along with the following packages:

- `requests`
- `bs4` (BeautifulSoup)
- `pika`
- `tinydb`

You can install these packages using `pip`:

```bash
pip install requests bs4 pika tinydb
```
Additionally, you will need to have RabbitMQ server running on your local machine or accessible remotely to use `rabbits.py` and `task_producer.py`.

## Usage

Each script is designed to be run independently. Here are the basic usage instructions for each:

`task_producer.py` can be run directly to parse links from the specified website and send them to the RabbitMQ queue for processing.
`rabbits.py` can be run directly to start the worker threads that will process tasks from the RabbitMQ queue.
