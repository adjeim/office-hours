import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, abort
from twilio.rest import Client
from tinydb import TinyDB, Query

load_dotenv()
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_API_KEY_SID = os.environ.get('TWILIO_API_KEY_SID')
TWILIO_API_KEY_SECRET = os.environ.get('TWILIO_API_KEY_SECRET')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')

client = Client(TWILIO_API_KEY_SID, TWILIO_API_KEY_SECRET, TWILIO_ACCOUNT_SID)
db = TinyDB('office_hours.json')
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods=['POST'])
def get_or_create_room():
    request_data = request.get_json()

    identity = request_data.get('identity')
    phone = request_data.get('phone')
    room_name = request_data.get('roomName')

    if not identity or not phone or not room_name:
        abort(400, 'Missing one of: identity, phone, room_name')

    # Try to get the room if it exists
    video_room_list = client.video.rooms.list(limit=20)
    found_video_rooms = [room for room in video_room_list if room.unique_name == room_name]
    video_room = found_video_rooms[0] if found_video_rooms else None

    # If the room does not exist, create a new one
    if not video_room:
        request_url = request.headers.get('referer')
        callback_url = f'{request_url}message'

        video_room = client.video.rooms.create(
            unique_name=room_name,
            empty_room_timeout=60,
            unused_room_timeout=60,
            status_callback=callback_url,
            status_callback_method='POST',
        )

    office_hours_appointment = {
        'identity': identity,
        'phone': phone,
        'room_name': video_room.unique_name,
        'room_sid': video_room.sid
    }

    # Check whether a record for this office hours meeting already exists
    office_hours_meeting = Query()
    selected_meeting = db.get(office_hours_meeting.room_sid == video_room.sid)

    # If a record does not exist, insert a new one
    if not selected_meeting:
        db.insert(office_hours_appointment)

    return {
        'video_room': {
            'sid': video_room.sid,
            'name': video_room.unique_name,
            'empty_room_timeout': video_room.empty_room_timeout,
            'unused_room_timeout': video_room.unused_room_timeout,
            'status_callback': video_room.status_callback
        }
    }


@app.route('/message', methods=['POST'])
def send_participant_notification():
    event = request.values.get('StatusCallbackEvent')

    if event == 'participant-connected':
        room_sid = request.values.get('RoomSid')

        office_hours_meeting = Query()

        # Query for the video meeting by its sid
        selected_meeting = db.get(office_hours_meeting.room_sid == room_sid)

        participant = request.values.get('ParticipantIdentity')
        room_name = selected_meeting.get('room_name')
        phone = selected_meeting.get('phone')
        identity = selected_meeting.get('identity')

        # Send an SMS to the creator of the video meeting
        message = client.messages.create(
            body=f'Hello {identity}! {participant} has joined your office hours room: {room_name}',
            from_=TWILIO_PHONE_NUMBER,
            to=phone
        )

        return {
            'status': 'Message sent!',
            'message_sid': message.sid,
        }

    return {
        'status': 'No message sent.',
    }