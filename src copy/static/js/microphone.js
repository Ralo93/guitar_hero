document.getElementById('start-listening').addEventListener('click', function() {
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

                mediaRecorder.ondataavailable = function(event) {
                    const reader = new FileReader();
                    reader.readAsDataURL(event.data);
                    reader.onloadend = function() {
                        const base64Audio = reader.result.split(',')[1]; // Get base64 audio data
                        
                        // Send audio data to the backend
                        fetch('/listen', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                audio_data: base64Audio
                            })
                        })
                        .then(response => response.json())
                        .then(data => {
                            // Update the displayed chord and recommendations
                            document.getElementById('chord-info').textContent = data.chord;
                            const recommendationsList = document.getElementById('recommendations-list');
                            recommendationsList.innerHTML = '';  // Clear previous recommendations
                            data.next_chords.forEach(chord => {
                                const li = document.createElement('li');
                                li.textContent = chord;
                                recommendationsList.appendChild(li);
                            });
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

                // Start the volume meter update loop
                updateVolume();

                // Start recording audio data
                mediaRecorder.start(1000);  // Record audio chunks every 1 second
            })
            .catch(err => console.log('Error accessing microphone: ', err));
    } else {
        console.log('getUserMedia not supported on your browser!');
    }
});
