import pika
import json
import re
import os

class MessageProducer:
    def __init__(self, file_path, queue_name, rabbitmq_url):
        self.file_path = file_path
        self.queue_name = queue_name
        self.rabbitmq_url = rabbitmq_url

    def send_to_queue(self, data):
        try:
            #connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))
            connection = pika.BlockingConnection(pika.URLParameters('amqp://guest:guest@host.docker.internal:5672/'))
            channel = connection.channel()

            json_data = json.dumps(data)
            # Declare the queue
            channel.queue_declare(queue=self.queue_name)

            channel.basic_publish(exchange='',
                                routing_key=self.queue_name,
                                body=json_data)
            print("Sent data to the queue")
            connection.close()
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Error connecting to RabbitMQ: {e}")
            print(f"URL: {self.rabbitmq_url}")
            raise  # Explicitly raise the exception
        except pika.exceptions.AMQPChannelError as e:
            print(f"Error on RabbitMQ channel: {e}")
            raise  # Explicitly raise the exception
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise  # Explicitly raise the exception

        
#os.getenv('RABBITMQ_QUEUE')
if __name__ == "__main__":
    file_path = 'assignment_updated.json'  # Replace with your file path
    queue_name =  os.getenv('RABBITMQ_QUEUE') # Use the queue name 'dw_queue'
    rabbitmq_url = os.getenv('RABBITMQ_URL')  # RabbitMQ URL

    print("123131")
    print(queue_name)

    producer = MessageProducer(file_path, queue_name, rabbitmq_url)
    temp_list = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = re.sub(r"}\s*{", "},{", file.read())

        temp_list.extend(json.loads("[" + json_data + "]"))

        for each_record in temp_list:
            print(each_record)
            producer.send_to_queue(each_record)

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
