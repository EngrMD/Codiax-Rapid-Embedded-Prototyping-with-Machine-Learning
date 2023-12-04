import paho.mqtt.publish as publish
import json
import random
import time

def generate_message():
    val = random.randint(1, 10)
    message = {"speed": val}
    return json.dumps(message)

def publish_message(broker_ip):
    topic = "my-topic"
    message = generate_message()
    
    publish.single(topic, message, hostname=broker_ip)
    print(f"Published: Topic - {topic}, Message - {message}")

if __name__ == "__main__":
    # Replace "your_broker_ip" with the actual IP address of your MQTT broker
    broker_ip = "127.0.0.1"

    while True:
        publish_message(broker_ip)
        time.sleep(5)  # Publish every 5 seconds, adjust as needed
