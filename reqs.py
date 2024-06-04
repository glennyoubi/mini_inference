import re
import requests
import json_converter
import os
import my_utils
import json

def get_jdm_page(term,relation=''):
    #check = check_node_already_exists(term, relation)
    check = check_node_already_exists_rels(term, relation)
    print(f"check : {check}")
    if check:
        print(f'{term} is in the database')

        

    else:
        # On récupère le contenu HTML de la page liée au mot recherché
        response = requests.get(f'https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel={term}&rel={relation}', verify=False)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Data fetched")
            print()
        else:
            print('Failed to fetch data:', response.status_code)
            raise SystemExit

        fichier_out_path = save_response(response.text, term, relation)
        
        extract_code_content(fichier_out_path)
        store_node_eid(fichier_out_path, relation)
        stores_nodes(fichier_out_path, term, relation)
        extract_relations_entrantes(fichier_out_path, term, relation)
        extract_relations_sortantes(fichier_out_path, term, relation)
        my_utils.delete_file(f'./words/{term}_{relation}_relations_entrantes.txt')
        my_utils.delete_file(f'./words/{term}_{relation}_relations_sortantes.txt')
        my_utils.delete_file(f'./words/{term}_all_nodes.txt')
        

def save_response(res,term_file_name,relation=''):
    response_file = open(f'./words/{term_file_name}_{relation}.txt', 'w')
    with open(f'./words/{term_file_name}_{relation}.txt', 'w') as file:
            # Write the response content to the file
        file.write(res)
        #print(f'Response saved to /words/{term_file_name}_{relation}.txt')
    if file.closed:
        print('File is closed')
        print()
    else:
        print('File is not closed')
    return f'./words/{term_file_name}_{relation}.txt'

def store_node_eid(file_path, relation):
    # This function save the eid of the node in a dictionnary so we can check if we already the value of a word in our database.

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Iterate through the lines to find the target line
    for line in lines:
        if line.startswith("// DUMP pour le terme"):
            # Use regex to extract the word between quotes and the number
            match = re.search(r"// DUMP pour le terme '([^']+)' \(eid=(\d+)\)", line)
            if match:
                key = match.group(1)  # The word between quotes
                value = int(match.group(2))  # The number as an integer
                check_node_already_exists_and_add(key, value, relation)
            break  # Exit the loop after finding the target line


def check_node_already_exists_and_add(new_word, new_value, relation=''):

    # Flag to check if the word is already present
    file_path = './words/words_base.txt'
    file_path_rels = './words/words_base_rels.txt'
    word_present = check_node_already_exists(new_word, relation)
    word_rels_present = check_node_already_exists_rels(new_word, relation)
    if not word_present:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f'{new_word} -> {new_value},{relation}\n')
            #print('added in database')
    else:
        print()
        #print(f"The word '{new_word}' is already present in the file.")

    if not word_rels_present:
        with open(file_path_rels, 'a', encoding='utf-8') as file:
            file.write(f'{new_word} -> {relation}\n')
            #print('added in database')
    else:
        print()
        #print(f"The word '{new_word}' is already present in the file.")

    return 2 # 2 means word is added

def check_node_already_exists(new_word, relation=''):

    # Flag to check if the word is already present
    word_present = False
    # for execution
    file_path = './words/words_base.txt'
    # for debugging
    # ff = 'requests/words/words_base.txt'
    # Read the file and check for the word
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        # Split the line into word and value
        if '->' in line:
            splitting1 = line.split(' -> ')
            splitting2 = line.split(',')
            #word, value, rel = line.split('->')
            
            #word = word.strip()
            #value = value.strip()
            #rel_w_newline = value.strip()
            
            word = splitting1[0]
            value = splitting1[1]
            #rel_w_newline = splitting2[1]
            #rel_without_newline = rel_w_newline.rstrip()
            # Check if the word is already in the res
            if word == new_word:
                word_present = True
                return word_present

    return word_present


def check_node_already_exists_rels(new_word, relation=''):
    # Flag to check if the word is already present
    word_present = False
    # for execution
    file_path = './words/words_base_rels.txt'
    # for debugging
    # ff = 'requests/words/words_base.txt'
    # Read the file and check for the word
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        # Split the line into word and value
        if '->' in line:
            splitting1 = line.split(' -> ')
            #splitting2 = line.split(',')
            #word, value, rel = line.split('->')
            
            #word = word.strip()
            #value = value.strip()
            #rel_w_newline = value.strip()
            
            word = splitting1[0]
            rel = splitting1[1]
            rel_without_newline = rel.rstrip()
            # Check if the word is already in the res
            if word == new_word and rel_without_newline == relation:
                word_present = True
                return word_present

    return word_present



def extract_code_content(file_path):
    # Open the file and read its content
    with open(file_path, 'r') as file:
        response = file.read()

    # Find the index of <CODE> and </CODE> tags
    start_index = response.find('<CODE>') + len('<CODE>')
    end_index = response.find('</CODE>')

    # Extract the content between <CODE> and </CODE> tags
    code_content = response[start_index:end_index]

    # We removing the .txt extension
    f_name_new = file.name[:-4]

    # Save the extracted content in a txt file
    save_to_txt(code_content, f'{file_path}')
    if code_content =='MUTED_PLEASE_RESEND':
        print('MUTED_PLEASE_RESEND')
        print('NO DATA AVAILABLE RELOAD THE PROGRAM')
        raise SystemExit
    return code_content

def extract_relations_entrantes(file_path, term, relation=''):
    # Open the file and read its content
    with open(file_path, 'r') as file:
        response = file.read()

    # Find the index of <CODE> and </CODE> tags
    start_index = response.find('// les relations entrantes :') + len('// les relations entrantes :')
    end_index = response.find('// END')

    # Extract the content between <CODE> and </CODE> tags
    code_content = response[start_index:end_index]

    # We removing the .txt extension
    file_path_wout_txt = file_path[:-4]
    file_path_wout_2_txt = file_path_wout_txt[2:]
    print(file_path_wout_txt)
    print(file_path_wout_2_txt)
    # Save the extracted content in a txt file
    save_to_txt(code_content, f'{file_path_wout_txt}_relations_entrantes.txt')
    json_converter.converter(f'{file_path_wout_txt}_relations_entrantes.txt', f'{file_path_wout_2_txt}_relations_entrantes.json', f'./words/relations/{term}_relations_entrantes_{relation}.json')
    # Return the extracted content
    return 1


def extract_relations_sortantes(file_path, term, relation=''):
    # Open the file and read its content
    with open(file_path, 'r') as file:
        response = file.read()

    # Find the index of <CODE> and </CODE> tags
    start_index = response.find('// les relations sortantes :') + len('// les relations sortantes :')
    end_index = response.find('// END')

    # Extract the content between <CODE> and </CODE> tags
    code_content = response[start_index:end_index]

    # We removing the .txt extension
    file_path_wout_txt = file_path[:-4]
    file_path_wout_2_txt = file_path_wout_txt[1:]
    print(file_path_wout_2_txt)
    # Save the extracted content in a txt file
    save_to_txt(code_content, f'{file_path_wout_txt}_relations_sortantes.txt')
    json_converter.converter(f'{file_path_wout_txt}_relations_sortantes.txt', f'{file_path_wout_2_txt}_relations_sortantes.json',f'./words/relations/{term}_relations_sortantes_{relation}.json' )
    # Return the extracted content
    return code_content

def save_to_txt(content, output_file):
    with open(output_file, 'w') as file:
        file.write(content)
    return

def stores_nodes(file_path, term, relation=''):
    input_filename = file_path
    with open(input_filename, "r") as file:
        data = file.read()

    # Use a regular expression to find all lines starting with "e;"
    pattern = re.compile(r'^e;.*', re.MULTILINE)
    filtered_lines = pattern.findall(data)

    # Write the filtered lines to a text file
    output_filename = "output.txt"
    with open(f'./words/{term}_all_nodes.txt', "w") as file:
        for line in filtered_lines:
            file.write(line + "\n")
    
    json_converter.parse_lines_to_dict(f'./words/{term}_all_nodes.txt', f'{term}_relations_sortantes.json',f'./words/relations/{term}_all_nodes_{relation}.json')
    return

def get_node_name_by_eid(node_eid, term, relation):
    name=''
    with open(f'./words/relations/{term}_all_nodes_{relation}.json', 'r') as f:
        data = json.load(f)
    for key1 in data:
        if key1 == node_eid:
            #print(data[key1]['name'])
            name = data[key1]['name']
    return name   

def get_node_eid_by_name(node_name, file_path):
    pass



    
if __name__ == "__main__":
    #get_jdm_page("chat")
    #get_jdm_page("chat", 6)
    #print(name)
    #t = check_node_already_exists('pizza','6')
    d = check_node_already_exists_rels('tour eiffel','15')
    #print(t)
    print(d)
    d = check_node_already_exists_rels('pizza','6')
    print(d)
