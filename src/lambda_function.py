import json

print('Loading function')



def lambda_handler(event, context):
    print(f"Received event: {event}")

    return event
