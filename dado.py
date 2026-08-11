import json
import random

def handler(event, context):
    resultado = random.randint(1, 6)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"resultado": resultado})
    }
