// static/js/microphone.js

document.getElementById('start-listening').addEventListener('click', function() {
    const listenButton = this; // Reference to the start-listening button
    const loadingIndicator = document.getElementById('loading-indicator'); // Loading indicator

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                const audioContext = new AudioContext();
                const analyser = audioContext.createAnalyser();
                const mediaRecorder = new MediaRecorder(stream);
                const source = audioContext.createMediaStreamSource(stream);
                source.connect(analyser);
                
                analyser.fftSize = 256;
                const bufferLength = analyser.frequencyBinCount;
                const dataArray = new Uint8Array(bufferLength);

                let recording = false; // Flag to indicate if recording is in progress

                mediaRecorder.ondataavailable = function(event) {
                    const reader = new FileReader();
                    reader.readAsDataURL(event.data);
                    reader.onloadend = function() {
                        const base64Audio = reader.result.split(',')[1]; // Get base64 audio data
                        
                        // Show loading indicator
                        loadingIndicator.style.display = 'block';

                        // Send audio data to the backend
                        fetch('/start_listening', {  // Ensure the endpoint matches Flask route
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                audio_data: base64Audio
                            })
                        })
                        .then(response => {
                            loadingIndicator.style.display = 'none'; // Hide loading indicator
                            return response.json();
                        })
                        .then(data => {
                            if (data.error) {
                                // Handle error returned from the server
                                document.getElementById('chord-info').textContent = 'Error: ' + data.error;
                                document.getElementById('recommendations-list').innerHTML = '<li>Error processing audio.</li>';
                            } else {
                                // Update the displayed chord and recommendations
                                document.getElementById('chord-info').textContent = data.chord;
                                const recommendationsList = document.getElementById('recommendations-list');
                                recommendationsList.innerHTML = '';  // Clear previous recommendations
                                data.next_chords.forEach(chord => {
                                    const li = document.createElement('li');
                                    li.textContent = chord;
                                    recommendationsList.appendChild(li);
                                });
                            }
                        })
                        .catch(error => {
                            loadingIndicator.style.display = 'none'; // Hide loading indicator
                            console.error('Error:', error);
                            document.getElementById('chord-info').textContent = 'Error: Unable to communicate with the server.';
                            document.getElementById('recommendations-list').innerHTML = '<li>Unable to communicate with the server.</li>';
                        });
                    }
                };

                function updateVolume() {
                    analyser.getByteTimeDomainData(dataArray);
                    let sum = 0;
                    for (let i = 0; i < bufferLength; i++) {
                        sum += Math.pow(dataArray[i] - 128, 2);
                    }
                    const rms = Math.sqrt(sum / bufferLength);  // Root mean square for volume level
                    const volume = Math.min(rms / 128, 1);  // Normalize volume between 0 and 1
                    const degree = -90 + (volume * 180);  // Map volume to degree for needle

                    // Update needle position
                    document.getElementById('volume-needle').style.transform = `rotate(${degree}deg)`;

                    // Update numerical volume display
                    document.getElementById('volume-display').textContent = Math.round(volume * 100);

                    // Call itself recursively for continuous update
                    requestAnimationFrame(updateVolume);
                }

                // Function to start recording
                function startRecording() {
                    if (recording) return; // Prevent multiple recordings
                    recording = true;
                    listenButton.disabled = true; // Disable the button during recording
                    listenButton.textContent = 'Listening...'; // Update button text

                    // Start the volume meter update loop
                    updateVolume();

                    // Start recording audio data
                    mediaRecorder.start();

                    // Stop recording after 2 seconds (2000 milliseconds)
                    setTimeout(() => {
                        mediaRecorder.stop();
                        recording = false;
                        listenButton.disabled = false; // Re-enable the button
                        listenButton.textContent = 'Start Listening'; // Reset button text
                        // Optionally, you can stop the audio stream here if you don't need it anymore
                        stream.getTracks().forEach(track => track.stop());
                    }, 2000);
                }

                // Start the recording process
                startRecording();
            })
            .catch(err => console.log('Error accessing microphone: ', err));
    } else {
        console.log('getUserMedia not supported on your browser!');
    }
});
