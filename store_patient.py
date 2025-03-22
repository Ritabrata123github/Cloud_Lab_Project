import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("patientData")

# Function to convert numbers to Decimal (for DynamoDB)
def convert_to_decimal(obj):
    if isinstance(obj, int) or isinstance(obj, float):
        return Decimal(str(obj))  # Convert numbers to Decimal
    if isinstance(obj, list):
        return [convert_to_decimal(i) for i in obj]
    if isinstance(obj, dict):
        return {k: convert_to_decimal(v) for k, v in obj.items()}
    return obj

def lambda_handler(event, context):
    try:
        # Ensure event["body"] is properly parsed
        body = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]

        # Extract values
        patient_id = body["patient_id"]
        name = body["name"]
        age = body["age"]
        medical_history = body["medical_history"]

        # Convert numbers before storing in DynamoDB
        item = convert_to_decimal({
            "patient_id": patient_id,
            "name": name,
            "age": age,
            "medical_history": medical_history
        })

        # Save patient data to DynamoDB
        table.put_item(Item=item)

        return {
            "statusCode": 200,
             "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
            "body": json.dumps({"message": "Patient record saved successfully!"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

