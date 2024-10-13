def recommend_next_chords(current_chord):
    # A simplified harmonic progression recommendation
    harmonic_map = {
    'C': ['F', 'G', 'Am', 'Em', 'Dm', 'C7', 'G7'],  # C major family
    'G': ['C', 'D', 'Em', 'Am', 'Bm', 'G7', 'D7'],  # G major family
    'D': ['G', 'A', 'Bm', 'Em', 'F#m', 'D7', 'A7'], # D major family
    'A': ['D', 'E', 'F#m', 'Bm', 'C#m', 'A7', 'E7'], # A major family
    'E': ['A', 'B', 'C#m', 'F#m', 'G#m', 'E7', 'B7'], # E major family
    'F': ['Bb', 'C', 'Dm', 'Gm', 'Am', 'F7', 'C7'],  # F major family
    'Am': ['Dm', 'Em', 'F', 'G', 'C', 'E7'],  # A minor family
    'Em': ['Am', 'Bm', 'C', 'D', 'G', 'B7'],  # E minor family
    'Dm': ['Gm', 'Am', 'C', 'F', 'Bb', 'A7'], # D minor family
}
    
    return harmonic_map.get(current_chord, [])
