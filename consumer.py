import pika
import psycopg2
import json
import os

class RabbitMQConsumer:
    def __init__(self, queue_name, rabbitmq_host=os.getenv('RABBITMQ_HOST'), rabbitmq_port=os.getenv('RABBITMQ_PORT')):
        self.queue_name = queue_name
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port
        self.connection = None
        self.channel = None

    def connect_to_rabbitmq(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.rabbitmq_host, port=self.rabbitmq_port)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name)
            print("Connected to RabbitMQ successfully!")
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Error connecting to RabbitMQ: {e}")
            print(f"Host: {self.rabbitmq_host}, Port: {self.rabbitmq_port}, Queue Name: {self.queue_name}")
            raise  # Explicitly raise the exception
        except pika.exceptions.AMQPChannelError as e:
            print(f"Error on RabbitMQ channel: {e}")
            raise  # Explicitly raise the exception
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise  # Explicitly raise the exception


    def consume_messages(self):
        try:
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_message_callback, auto_ack=True)
            print("Waiting for messages. To exit, press CTRL+C")
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print("Stopped consuming messages.")
            self.channel.stop_consuming()  # Stop consuming messages explicitly
        except Exception as e:
            print(f"Error consuming from RabbitMQ: {str(e)}")
            raise
        finally:
            self.close_rabbitmq_connection()  # Close RabbitMQ connection


    def close_rabbitmq_connection(self):
        try:
            if self.channel:
                self.channel.close()  # Close the channel
            if self.connection and not self.connection.is_closed:
                self.connection.close()  # Close the connection
            print("RabbitMQ connection closed.")
        except Exception as e:
            print(f"Error closing RabbitMQ connection: {str(e)}")
            raise


    def on_message_callback(self, channel, method, properties, body):
        try:
            print("Received message:", body)
            if body:
                sanitized_data = self.sanitize_data(body.decode())
                print("Sanitized data:", sanitized_data)
                self.write_to_postgres(sanitized_data)
                print("Data processed and inserted into PostgreSQL.")
        except Exception as e:
            print(f"Error consuming message and writing to PostgreSQL: {str(e)}")
            raise

    def sanitize_data(self, data):
        # Implement your data sanitization logic here
        # Example: Removing special characters
        sanitized_data = data.replace('#', '')
        return sanitized_data

    def write_to_postgres(self, data):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                host=os.getenv('POSTGRES_HOST'),
                port=os.getenv('POSTGRES_PORT')
            )
            cursor = conn.cursor()
            print("Connected to PostgreSQL database successfully!")

            data = eval(data)
            meta_info = data.get('meta_info', {})

            if isinstance(meta_info, str):
                meta_info = json.loads(meta_info.replace("'", '"'))

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dw_test_table (
                    id SERIAL PRIMARY KEY,
                    index INTEGER,
                    meta_info JSONB,
                    available_price VARCHAR(50),
                    stock VARCHAR(50),
                    source VARCHAR(50)
                )
            ''')

            cursor.execute(
                "INSERT INTO dw_test_table (index, meta_info, available_price, stock, source) VALUES (%s, %s, %s, %s, %s)",
                (data['index'], json.dumps(meta_info), data['available_price'], data['stock'], data['source'])
            )
            conn.commit()
            cursor.close()
            conn.close()
            print("Data uploaded successfully!")
        except Exception as e:
            print(f"Error writing to PostgreSQL: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        consumer = RabbitMQConsumer(queue_name='dw_queue')
        consumer.connect_to_rabbitmq()
        consumer.consume_messages()
    except Exception as e:
        print(f"An error occurred: {str(e)}")



