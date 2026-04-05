import boto3
from botocore.exceptions import ClientError
from app.config import settings

# Initialize DynamoDB resource lazily
dynamodb = None
table = None

def get_table():
    global dynamodb, table
    if dynamodb is None:
        dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION)
        table = dynamodb.Table(settings.DYNAMODB_SESSIONS_TABLE)
    return table

def get_session_history(session_id: str, limit: int = 10) -> list:
    """
    Fetches the chat history array from DynamoDB for a specific session_id.
    Returns the array properly formatted for Bedrock Converse.
    """
    if not session_id:
        return []
        
    try:
        response = get_table().get_item(Key={'session_id': session_id})
        item = response.get('Item')
        if item and 'history' in item:
            # Return only the last `limit` messages to save context tokens
            return item['history'][-limit:]
        return []
    except ClientError as e:
        print(f"DynamoDB GetItem Error: {e}")
        return []

def save_interaction(session_id: str, user_text: str, assistant_text: str):
    """
    Appends the latest Q&A interaction to the user's DynamoDB history list.
    If the session_id doesn't exist, it creates a new record.
    """
    if not session_id:
        return
        
    # Format messages exactly as Bedrock Converse expects them
    new_messages = [
        {"role": "user", "content": [{"text": user_text}]},
        {"role": "assistant", "content": [{"text": assistant_text}]}
    ]

    try:
        # Atomic append to the history list, creating the item and list if it doesn't exist
        get_table().update_item(
            Key={'session_id': session_id},
            UpdateExpression="SET history = list_append(if_not_exists(history, :empty_list), :new_messages)",
            ExpressionAttributeValues={
                ':empty_list': [],
                ':new_messages': new_messages
            }
        )
    except ClientError as e:
        print(f"DynamoDB UpdateItem Error: {e}")
