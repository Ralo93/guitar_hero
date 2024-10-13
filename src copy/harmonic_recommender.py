def recommend_next_chords(current_chord):
    # A simplified harmonic progression recommendation
    harmonic_map = {
        'C': ['F', 'G', 'Am'],
        'G': ['C', 'D', 'Em'],
        # Add more based on harmonic theory
    }
    
    return harmonic_map.get(current_chord, [])
