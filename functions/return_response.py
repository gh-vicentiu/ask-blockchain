import httpx
import asyncio

async def send_message_to_hook_async(user_id, messaged_back):
    url = 'http://localhost:5000/receive_update'
    data = {
        'user_id': user_id,
        'messaged_back': messaged_back
    }
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json=data)
        except httpx.RequestError as e:
            print(f"Error sending message: {e}")
