import os
import shutil

def remove_all_json(directory):
    # Define the directory and the file to keep
    directory = './words/relations'
    file_to_keep = 'keep.txt'

    # Loop through the files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        # Check if the current file is the one to keep
        if filename != file_to_keep:
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                pass

def remove_all_txt():

    # Define the directory and the file to keep
    directory = './words'
    file_to_keep = 'words_base.txt'

    # Loop through the files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        # Check if the current file is the one to keep
        if filename != file_to_keep:
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                pass
    
def clean_words_base():
    # Specify the path to your file
    file_path = './words/words_base.txt'

    # Open the file in write mode, which will truncate its contents
    with open(file_path, 'w') as file:
        pass  # The file is now empty

def clean_words_base_rels():
    # Specify the path to your file
    file_path = './words/words_base_rels.txt'

    # Open the file in write mode, which will truncate its contents
    with open(file_path, 'w') as file:
        pass  # The file is now empty

    





if __name__ == '__main__':
    repository_path = './words/relations'
    remove_all_json(repository_path)
    remove_all_txt()
    clean_words_base()
    clean_words_base_rels()