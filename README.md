
# Real-Time Guitar Chord Classification & Harmonic Recommendations

This project provides real-time guitar chord classification and harmonic recommendations to guide your next chord choice. Using transfer learning from a pre-trained VGGish model, the system classifies chords played on the guitar. It then suggests the next best chord based on harmonic principles like the Circle of Fifths or common progressions (e.g., I-IV-V).

## Features

- **Real-time Chord Classification**: Detect chords in real-time using transfer learning from a pre-trained Convolutional Neural Network (CNN) (VGGish).
- **Harmonic Recommendations**: Get recommendations for the next chord based on harmonic relationships. Suggestions leverage harmonic theory, such as:
  - Circle of Fifths
  - Common progressions (I-IV-V, ii-V-I, etc.)
  - Other harmonic rules
- **Graph Database for Harmonic Relationships**: A graph database is used to represent and query chord relationships, enabling flexible and contextually accurate recommendations.

## How It Works

1. **Chord Classification**: The VGGish model, originally trained on general audio features, has been fine-tuned to classify guitar chords. This model listens to your guitar input and predicts the chord being played in real-time.
   
2. **Harmonic Graph Representation**: Chord relationships and harmonic progressions are stored in a graph database. This allows for fast retrieval of the most harmonically appropriate chords to follow the current one. A graph database is ideal here due to the highly interconnected nature of chords and their relationships, making it easy to traverse and find the next best option.

3. **Recommendations**: Based on the detected chord and the graph of harmonics, the system suggests possible next chords. This recommendation can be tailored to specific progressions or harmonic preferences (e.g., sticking to diatonic chords or exploring borrowed chords).

## Installation

To get started with this project, follow these steps:

1. **Clone the repository**:
    \`\`\`bash
    git clone https://github.com/your-username/realtime-chord-classification.git
    cd realtime-chord-classification
    \`\`\`

2. **Install dependencies**:
    Ensure you have Python 3.x installed, then run:
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`

3. **Set up Graph Database**:
    Install and set up the graph database of your choice (e.g., Neo4j). Populate the database with chord relationships based on harmonic theory (a pre-made dataset can be provided in the repository).

4. **Run the Application**:
    Once the environment is set up, run the chord classifier and harmonics recommender with:
    \`\`\`bash
    python app.py
    \`\`\`

## Usage

- **Classification**: Play a chord on your guitar, and the model will classify it in real-time.
- **Recommendation**: After classification, the system will provide several recommended next chords based on harmonic relationships.

## Technologies Used

- **CNN (VGGish)**: Used for feature extraction from audio data. Transfer learning fine-tunes the model to classify guitar chords.
- **Graph Database (e.g., Neo4j)**: Stores harmonic relationships between chords. Efficiently queries for recommendations based on the detected chord.
- **Python**: Backend logic for classification and graph traversal.
- **Flask/Streamlit (optional)**: If a web-based interface is used for real-time interaction and visualization.

## Future Work

- Expanding the chord vocabulary to include more complex jazz chords.
- Introducing user-configurable settings for harmonic suggestions (e.g., choosing between diatonic and chromatic suggestions).
- Visualizing chord progressions in real-time using the Circle of Fifths or another music theory framework.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
