# account/utils.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_notification_to_user(user_id, title, message):
    """
    Sends a real-time notification to a specific user via WebSocket.
    """
    channel_layer = get_channel_layer()
    group_name = f"user_{user_id}"

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_notification",
            "title": title,
            "message": message,
        }
    )
