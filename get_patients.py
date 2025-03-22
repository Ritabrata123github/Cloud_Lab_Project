import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("patientData")

# Function to convert Decimal to int/float for JSON serialization
def convert_decimal(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)  # Convert to int if whole number, else float
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    if isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    return obj

def lambda_handler(event, context):
    try:
        response = table.scan()
        patients = response["Items"]

        return {
            "statusCode": 200,
             "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
            "body": json.dumps(convert_decimal(patients))  # Convert Decimal before returning JSON
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
