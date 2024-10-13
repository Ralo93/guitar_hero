# app.py
from flask import Flask, render_template, request, jsonify
from chord_recognition import recognize_chord
from harmonic_recommender import recommend_next_chords
import numpy as np
import base64
import io
from scipy.io import wavfile
#from flask_cors import CORS  # If needed

app = Flask(__name__)
# Uncomment the next line if you're facing CORS issues
# CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_listening', methods=['POST'])
def start_listening():
    try:
        # Receive base64 audio data from the frontend
        audio_data = request.json.get('audio_data')
        if not audio_data:
            return jsonify({'error': 'No audio data provided'}), 400

        # Decode base64 audio
        audio_decoded = base64.b64decode(audio_data)

        print("Audio data decoded successfully.")

        # Convert audio data to np.float32 (assumes it is in WAV format or raw PCM)
        audio_buffer = io.BytesIO(audio_decoded)
        try:
            sample_rate, audio_np = wavfile.read(audio_buffer)
            print(f"Audio data read as WAV. Sample rate: {sample_rate} Hz")
        except ValueError:
            # If the audio is not in WAV format, assume raw PCM
            if len(audio_decoded) % 2 != 0:
                audio_decoded += b'\x00'  # Padding the buffer if needed

            # Convert the buffer to an np array, assuming int16 PCM format
            audio_np = np.frombuffer(audio_decoded, dtype=np.int16).astype(np.float32)
            sample_rate = 44100  # Default sample rate; adjust as needed
            print(f"Audio data read as raw PCM. Sample rate assumed: {sample_rate} Hz")

        # Normalize the audio to the range -1.0 to 1.0
        if np.max(np.abs(audio_np)) == 0:
            return jsonify({'error': 'Audio data is silent'}), 400
        audio_np = audio_np / np.max(np.abs(audio_np), axis=0)

        print(f"Audio data normalized.")

        # Chord recognition
        chord = recognize_chord(audio_np, sample_rate)
        print(f"Recognized Chord: {chord}")

        # Chord recommendation
        next_chords = recommend_next_chords(chord)
        print(f"Recommended Next Chords: {next_chords}")

        # Return results as JSON
        return jsonify({
            'chord': chord,
            'next_chords': next_chords
        }), 200

    except Exception as e:
        print(f"Error processing audio: {e}")
        return jsonify({
            'error': 'Failed to process audio data'
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
