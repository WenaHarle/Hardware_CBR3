from aws_iot import AWSIoTClient

if __name__ == "__main__":
    aws_iot_client = AWSIoTClient()
    aws_iot_client.connect()

    # Your MQTT operations here...
    aws_iot_client.publish("topic/test", "Hello from AWS IoT Core")

    # Define your callback function for receiving messages
    def callback(client, userdata, message):
        print("Received message payload:", message.payload.decode())

    # Subscribe to a topic
    aws_iot_client.subscribe("topic/test", callback)

    # You can call more publish or subscribe methods as needed

    # Clean up resources
    aws_iot_client.cleanup()
