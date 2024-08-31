import boto3
import boto3.session
import json

from session import SessionProvider

session_provider = SessionProvider()
session = session_provider.get_session()
queue_name = "vish-0"
queue_url = ""

# queue_two = "vish-1"
# queue_two_url = ""

fifo = "vish.fifo"
fifo_url = ""

# init sqs
sqs = session.resource("sqs")

sample_json = {
    "Title": "You have a new message!",
    "Body": "Hello, this is a test message from Vishwesh!",
}

message_attributes = {
    "Author": {"StringValue": "ChatGPT", "DataType": "String"},
    "Priority": {"StringValue": "High", "DataType": "String"},
}

# create first queue
queue_one_object = sqs.create_queue(QueueName=queue_name)
queue_url = queue_one_object.url

# create second queue
# queue_two_object = sqs.create_queue(QueueName=queue_two)
# queue_two_url = queue_two_object.url

# create fifo queue
fifo_object = sqs.create_queue(
    QueueName=fifo,
    Attributes={"FifoQueue": "true", "ContentBasedDeduplication": "true"},
)
fifo_url = fifo_object.url

try:
    sqs_client = session.client("sqs")
    create_q_res = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(sample_json),
        MessageAttributes=message_attributes,
    )
    print(f"Created queue: {queue_url}")
    print(f"Created fifo queue: {fifo_url}")
    print(f'Created message: {create_q_res["MessageId"]}')

    print("Polling now...")

    receive_message = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=20,
        MessageAttributeNames=["All"],
    )

    if "Messages" in receive_message:
        for message in receive_message["Messages"]:
            print(f"Message ID: {message['MessageId']}")
            print(f"Body: {message['Body']}")
            print(f"Attributes: {message.get('MessageAttributes', {})}")
            sqs_client.delete_message(
                QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"]
            )
            print("Message deleted.")
    else:
        print("No messages received.")

except Exception as e:
    print(f"*** Exception: {e}")
