def update_file_config(file_path, key, value):
    # Read the file contents
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
    # Iterate through lines and update the key if found
        for line in lines:
            if key in line:
                file.write(key + '=' + value + '\n')
            # If key is not found, it is added at the end of the file
            else:
                file.write(line)

server_config_file = r"C:\Users\dhanasekar\OneDrive\Documents\Python Scripts\Python_Scripts\File_Operations\server.conf"

key_to_update = 'max_connections'
new_value = '200'

update_file_config(server_config_file, key_to_update, new_value)