from flask import Flask, request
import os
from flask_cors import CORS,cross_origin
import json
from model import continual_chat, createVectorDB
from langchain_core.messages import HumanMessage, SystemMessage
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
from dotenv import load_dotenv
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Folder to save uploaded audio files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Deepgram API Key - Replace with your actual key
DEEPGRAM_API_KEY = os.getenv('DEEPGRAMAPI')


# Path to the audio file
AUDIO_FILE = "uploads/recording.wav"

chat_history = []

def transcribe_audio():
    try:
        # STEP 1 Create a Deepgram client using the API key
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)

        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        #STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        # STEP 3: Call the transcribe_file method with the text payload and options
        response = deepgram.listen.rest.v("1").transcribe_file(payload, options)

        # STEP 4: Print the response
        # print(response.to_json(indent=4))
        
        data = response.to_json()
        data = json.loads(data)
        transcript = data["results"]["channels"][0]["alternatives"][0]["transcript"]
        return transcript

    except Exception as e:
        print(f"Exception: {e}")


# Flask route to handle audio file uploads
@app.route('/upload-audio', methods=['POST'])
@cross_origin(origin='*')
def upload_audio():
    if 'audio' not in request.files:
        return "No file part", 400

    file = request.files['audio']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    print("Audio file uploaded successfully")

    # Run the async transcribe_audio function in an event loop
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # transcription_result = loop.run_until_complete(transcribe_audio(file_path))
    transcript = transcribe_audio()
    print(f"Transcription result: {transcript}")
    result = continual_chat(transcript,chat_history)
    chat_history.append(HumanMessage(content=transcript))
    chat_history.append(SystemMessage(content=result["answer"]))
    # print(f"Transcription result: {transcription_result}")

    # Return transcription result to the client
    return result['answer'], 200

@app.route('/submit-text', methods=['POST'])
def submit_text():
    data = request.get_json()  # Get JSON data from the request body
    text = data.get('text')  # Extract the 'text' from the JSON payload
    if text:
        print(f"Received text: {text}")
        result = continual_chat(text,chat_history)
        chat_history.append(HumanMessage(content=text))
        chat_history.append(SystemMessage(content=result["answer"]))
        print(result)
        return result['answer'], 200
    else:
        return "No text received", 400

# Run the Flask app
if __name__ == '__main__':
    createVectorDB()
    app.run(port=5000, debug=True)