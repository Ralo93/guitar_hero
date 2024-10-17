import os

def add_minor_to_filenames(directory_path):
    """
    This function adds '-Minor' to all filenames in the specified directory.
    
    :param directory_path: Path to the directory where files are located
    """
    try:
        # Loop through all files in the specified directory
        for filename in os.listdir(directory_path):
            # Construct full file path
            full_file_path = os.path.join(directory_path, filename)
            
            # Check if it is a file (not a directory)
            if os.path.isfile(full_file_path):
                # Add '-Minor' before the file extension
                name, ext = os.path.splitext(filename)
                new_name = f"{name}-Minor{ext}"
                
                # Construct full new file path
                new_file_path = os.path.join(directory_path, new_name)
                
                # Rename the file
                os.rename(full_file_path, new_file_path)
                
        print(f"All filenames in '{directory_path}' updated successfully.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
add_minor_to_filenames("/path/to/directory")  # Replace with your directory path
