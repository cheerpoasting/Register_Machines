import os

def openfile(file_name, allowed_extensions=(".txt",)): 

    if os.path.isdir(file_name):
        print(f"Error: '{os.path.basename(file_name)}' is a directory, not a file.")
        exit(400)  # 400 = Bad Request

    if not file_name.endswith(allowed_extensions):
        print(f"Error: '{os.path.basename(file_name)}' is not a supported file type, such as {allowed_extensions}.")
        exit(415) # invalid media type

    try: 
        if os.path.getsize(file_name) == 0:
            print(f"Error: '{os.path.basename(file_name)}' is empty.")
            exit(204) # 204 == No Content

        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: '{os.path.basename(file_name)}' not found.")
        exit(404) # 404 = File Not Found
    except UnicodeDecodeError:
        print(f"Error: '{os.path.basename(file_name)}' is not valid UTF-8.")
        exit(415) # 415 = Unsupported Media Type
    except PermissionError:
        print(f"Error: '{os.path.basename(file_name)}' cannot be read (permission denied).")
        exit(403)  # 403 = Forbidden

if __name__ == "__main__":
    file = input("File to Open: ")
    if file.lower() == "quit":
        exit(0) # normal exit
    openfile(file)