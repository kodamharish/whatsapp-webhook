from django.shortcuts import render

# Create your views here.

# webhook/views.py



# webhook/views.py

import json
import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Message

# Hardcoded sensitive tokens (Not Recommended)
WEBHOOK_VERIFY_TOKEN = 'harish'
GRAPH_API_TOKEN = 'EAAqJlXY27X4BOZBpv9UT9JTQL3fuQyXQaVTK73pAO6hDOnuBZCjDaAqxMq42bjFzlF6ebMtdXckiRO6ZCPOmS3zqtOttLCxlzCKo0DPwPZBebijdWIIqGXPTYB3ta9plujwndKtlCl7yu8cad19CrxjYKGgANSofhAzTCIpbxebHW4MPFiP9KWRlYDiYZBZBnykgZDZD'
PORT = 8000  # Note: Typically, PORT is managed by the server or deployment environment

# To store the latest message
latest_message = {}




@csrf_exempt
def webhook1(request):
    global latest_message

    if request.method == 'GET':
        # Handle webhook verification
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode == 'subscribe' and token == WEBHOOK_VERIFY_TOKEN:
            print("Webhook verified successfully!")
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse(status=403)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(status=400)

        # Extract message details
        message = data.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}).get('messages', [{}])[0]

        if message.get('type') == 'text':
            phone_number = message.get('from')  # Sender's WhatsApp ID
            message_body = message.get('text', {}).get('body')

            # Store the latest message
            latest_message = {
                'phoneNumber': phone_number,
                'messageBody': message_body
            }

            # Log the message details
            print(json.dumps(latest_message, indent=2))

            # Extract the business phone number ID
            business_phone_number_id = data.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}).get('metadata', {}).get('phone_number_id')

            if not business_phone_number_id:
                print("Business phone number ID not found.")
                return HttpResponse(status=400)

            # Send a reply message using the WhatsApp API
            reply_payload = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "text": {"body": "We will contact you as soon as possible - TZP"},
                "context": {
                    "message_id": message.get('id')
                }
            }

            headers = {
                "Authorization": f"Bearer {GRAPH_API_TOKEN}",
                "Content-Type": "application/json"
            }

            try:
                # Send the reply message
                response = requests.post(
                    f"https://graph.facebook.com/v18.0/{business_phone_number_id}/messages",
                    headers=headers,
                    json=reply_payload
                )
                response.raise_for_status()

                # Mark the message as read
                read_payload = {
                    "messaging_product": "whatsapp",
                    "status": "read",
                    "message_id": message.get('id')
                }

                read_response = requests.post(
                    f"https://graph.facebook.com/v18.0/{business_phone_number_id}/messages",
                    headers=headers,
                    json=read_payload
                )
                read_response.raise_for_status()

            except requests.exceptions.RequestException as e:
                print(f"Error sending messages: {e}")
                return HttpResponse(status=500)

        return HttpResponse(status=200)

    else:
        return HttpResponse(status=405)  # Method Not Allowed





def home1(request):
    if latest_message:
        return JsonResponse(latest_message)
    else:
        return JsonResponse({"message": "No messages received yet."})



@csrf_exempt
def webhook(request):
    if request.method == 'GET':
        # Handle webhook verification
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode == 'subscribe' and token == WEBHOOK_VERIFY_TOKEN:
            print("Webhook verified successfully!")
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse(status=403)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(status=400)

        # Extract message details
        entry = data.get('entry', [])
        if not entry:
            return HttpResponse(status=400)

        changes = entry[0].get('changes', [])
        if not changes:
            return HttpResponse(status=400)

        value = changes[0].get('value', {})
        messages = value.get('messages', [])
        if not messages:
            return HttpResponse(status=200)  # No message to process

        message = messages[0]
        message_type = message.get('type')

        if message_type == 'text':
            phone_number = message.get('from')  # Sender's WhatsApp ID
            message_body = message.get('text', {}).get('body')

            if not phone_number or not message_body:
                return HttpResponse(status=400)

            # Save the message to the database
            try:
                Message.objects.create(
                    phone_number=phone_number,
                    message_body=message_body
                )
            except Exception:
                return HttpResponse(status=500)

            # Extract the business phone number ID
            metadata = value.get('metadata', {})
            business_phone_number_id = metadata.get('phone_number_id')

            if not business_phone_number_id:
                print("Business phone number ID not found.")
                return HttpResponse(status=400)

            # Send a reply message using the WhatsApp API
            reply_payload = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "text": {"body": "We will contact you as soon as possible - TZP"},
                "context": {
                    "message_id": message.get('id')
                }
            }

            headers = {
                "Authorization": f"Bearer {GRAPH_API_TOKEN}",
                "Content-Type": "application/json"
            }

            try:
                # Send the reply message
                response = requests.post(
                    f"https://graph.facebook.com/v18.0/{business_phone_number_id}/messages",
                    headers=headers,
                    json=reply_payload
                )
                response.raise_for_status()

                # Mark the message as read
                read_payload = {
                    "messaging_product": "whatsapp",
                    "status": "read",
                    "message_id": message.get('id')
                }

                read_response = requests.post(
                    f"https://graph.facebook.com/v18.0/{business_phone_number_id}/messages",
                    headers=headers,
                    json=read_payload
                )
                read_response.raise_for_status()

            except requests.exceptions.RequestException as e:
                print(f"Error sending messages: {e}")
                return HttpResponse(status=500)

        return HttpResponse(status=200)

    else:
        return HttpResponse(status=405)  # Method Not Allowed

def home(request):
    # Fetch the latest message from the database
    latest_message = Message.objects.order_by('-timestamp').first()

    if latest_message:
        data = {
            'phoneNumber': latest_message.phone_number,
            'messageBody': latest_message.message_body,
            'timestamp': latest_message.timestamp
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"message": "No messages received yet."})