import json
import re

def converter(file_path, path_to_save,term):

    file_name =''


    with open(file_path, 'r') as file:
        data_string = file.read()
        file_name = file.name

    # Split the string into lines and remove empty lines
    lines = [line.strip() for line in data_string.strip().split('\n') if line.strip()]

    # Extract the keys from the first line and remove leading/trailing spaces
    keys = [key.strip() for key in lines[0].split(';')]

    # Initialize an empty dictionary to store data
    data = {}

    # Iterate over lines starting from line 2
    for line_number, line in enumerate(lines[2:], start=1):
        # Split the line into elements and remove leading/trailing spaces
        elements = [element.strip() for element in line.split(';')]
        
        # Create a dictionary using keys and elements
        line_data = {key: value for key, value in zip(keys[1:], elements[1:])}
        
        # Append the dictionary to the list associated with the key "r{line_number}"
        data[f"r{line_number}"] = [line_data]

    # Save data to a JSON file
    output_file = term
    with open(f'{output_file}', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    #print(f"JSON data saved to {output_file}")
    
    return output_file


def parse_lines_to_dict(file_path, path_to_save, term):
    # Read the input data from a file
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Parse the lines and create the dictionary
    # data_dict = parse_lines_to_dict(lines)

    # Write the dictionary to a JSON file
    output_filename = term
    

    # print(f"Data has been written to {output_filename}")
    data_dict = {}
    pattern = re.compile(r"^e;(\d+);'([^']+)';(\d+);(\d+)(?:;'([^']+)')?")
    for line in lines:
        match = pattern.match(line)
        if match:
            eid, name, type_, w, formatted_name = match.groups()
            data_dict[eid] = {
                "name": name,
                "type": int(type_),
                "w": int(w),
                "formatted_name": formatted_name
            }
    
    with open(output_filename, "w") as json_file:
        json.dump(data_dict, json_file, indent=4, ensure_ascii=False)

    return data_dict

