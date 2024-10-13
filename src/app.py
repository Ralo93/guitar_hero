from flask import Flask, render_template, request, jsonify
from chord_recognition import recognize_chord
from harmonic_recommender import recommend_next_chords
import numpy as np
import base64
import io
from scipy.io import wavfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listen', methods=['POST'])
def listen():
    # Receive base64 audio data from the frontend
    audio_data = request.json['audio_data']
    
    # Decode base64 audio
    audio_decoded = base64.b64decode(audio_data)

    print("encoded")
    
    # Convert audio data to np.float32 (assumes it is in raw format, like PCM)
    try:
        # Check the length of the decoded buffer is valid for int16 conversion
        if len(audio_decoded) % 2 != 0:
            audio_decoded += b'\x00'  # Padding the buffer if needed

        # Now convert the buffer to an np array, assuming int16 PCM format
        audio_np = np.frombuffer(audio_decoded, dtype=np.int16).astype(np.float32)

        # Normalize the audio to the range -1.0 to 1.0 (as audio is usually in this range for float)
        audio_np = audio_np / np.max(np.abs(audio_np), axis=0)

        # Chord recognition
        #chord = recognize_chord(audio_np)

        # Chord recommendation
        #next_chords = recommend_next_chords(chord)

        # Return results as JSON
        return jsonify({
            'chord': chord,
            'next_chords': next_chords
        })

    except Exception as e:
        print(f"Error processing audio: {e}")
        return jsonify({
            'error': 'Failed to process audio data'
        })

if __name__ == "__main__":
    app.run(debug=True)
