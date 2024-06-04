import os
import shutil

def delete_file(file_path):
   
    try:
        # Check if the file exists before trying to delete it
        if os.path.exists(file_path):
            os.remove(file_path)
            #print(f"{file_path} has been deleted successfully.")
        else:
            print(f"The file {file_path} does not exist.")
    except PermissionError:
        print(f"Permission denied: unable to delete {file_path}.")
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while trying to delete {file_path}: {e}")
        
