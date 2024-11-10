# from flask import Flask, request
# import os
# from flask_cors import CORS  # Importing CORS from flask_cors

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/upload-audio', methods=['POST'])
# def upload_audio():
#     if 'audio' not in request.files:
#         return "No file part", 400

#     file = request.files['audio']
#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(file_path)

#     print("Audio file uploaded successfully")
#     return "File uploaded successfully", 200

# @app.route('/submit-text', methods=['POST'])
# def submit_text():
#     data = request.get_json()  # Get JSON data from the request body
#     text = data.get('text')  # Extract the 'text' from the JSON payload
#     if text:
#         print(f"Received text: {text}")
#         return "Text received successfully", 200
#     else:
#         return "No text received", 400

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)



# Asynchronous function for audio transcription
# async def transcribe_audio(file_path):
#     try:
#         # Open the audio file
#         with open(file_path, "rb") as audio_file:
#             # Make an HTTP request to Deepgram's API
#             headers = {"Authorization": f"Token {DEEPGRAM_API_KEY}"}
#             files = {"file": audio_file}
#             params = {
#                 "model": "nova",  # Specify the model
#                 "smart_format": "true",  # Enable smart formatting
#             }
#             async with httpx.AsyncClient() as client:
#                 response = await client.post(
#                     "https://api.deepgram.com/v1/listen",
#                     headers=headers,
#                     params=params,
#                     files=files,
#                 )
            
#             # Handle the response
#             response.raise_for_status()
#             return response.json()  # Return JSON response

#     except httpx.HTTPStatusError as http_error:
#         print(f"HTTP error occurred: {http_error}")
#         return {"error": f"HTTP error occurred: {http_error}"}

#     except Exception as e:
#         print(f"Exception: {e}")
#         return {"error": f"Error transcribing audio: {e}"}




# from flask import Flask, request
# import os
# from flask_cors import CORS  # Importing CORS from flask_cors
# import torch
# from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
# import soundfile as sf
# import librosa
# from moviepy.editor import VideoFileClip

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Function to extract and transcribe speech from video/audio
# def extract_and_transcribe(audio_file_path):
#     print("Starting...")
#     # If the input is an audio file (wav, mp3), we can directly process it
#     # If it's a video, we'd extract the audio first
#     audio_file_path = "recording.wav"  # You can modify this path
#     # Assuming the input file is audio already; if it's video, you can extract as needed

#     device = "cuda:0" if torch.cuda.is_available() else "cpu"
#     torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
#     model_id = "openai/whisper-large-v3"

#     model = AutoModelForSpeechSeq2Seq.from_pretrained(
#         model_id, torch_dtype=torch_dtype, use_safetensors=True
#     )
#     model.to(device)

#     processor = AutoProcessor.from_pretrained(model_id)

#     pipe = pipeline(
#         "automatic-speech-recognition",
#         model=model,
#         tokenizer=processor.tokenizer,
#         feature_extractor=processor.feature_extractor,
#         max_new_tokens=128,
#         chunk_length_s=30,
#         batch_size=16,
#         return_timestamps=True,
#         torch_dtype=torch_dtype,
#         device=device,
#     )

#     def transcribe_audio(audio_path):
#         result = pipe(audio_path)
#         return result["text"]

#     transcription = transcribe_audio(audio_file_path)
#     return transcription

# @app.route('/upload-audio', methods=['POST'])
# def upload_audio():
#     if 'audio' not in request.files:
#         return "No file part", 400

#     file = request.files['audio']
#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(file_path)

#     print("Audio file uploaded successfully")

#     # Now process the uploaded audio for transcription
#     transcription = extract_and_transcribe(file_path)
#     print(f"Transcription: {transcription}")

#     return f"File uploaded successfully. Transcription: {transcription}", 200

# @app.route('/submit-text', methods=['POST'])
# def submit_text():
#     data = request.get_json()  # Get JSON data from the request body
#     text = data.get('text')  # Extract the 'text' from the JSON payload
#     if text:
#         print(f"Received text: {text}")
#         return {"message": "Text received successfully"}, 200
#     else:
#         return {"error": "No text received"}, 400

# # Run the Flask app
# if __name__ == '__main__':
#     app.run(port=5000, debug=True)
