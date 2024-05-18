import os, re, json, sys
from file_rename import rename_folder
from api.metron import Metron, Series

class Settings:
    def __init__(self, username, password, last_run):
        self.username = username
        self.password = password
        self.last_run = last_run

def save_settings():

    filename = 'settings.json'
    data = read_settings()

    # Update a dictionary to store the last run time
    #data["last_run"] = dt.now().timestamp()

    # Write the dictionary to a JSON file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def read_settings():
    # Define the filename
    filename = 'settings.json'
    data = {}

    # Read the JSON file into a dictionary
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"{filename} not found. Make sure the file exists.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {filename}.")
        sys.exit(1)
    return data


def get_volume_id(text):
    match = re.search(r'\{mt-(\d+)}', text)
    if match:
        return match.group(1)
    else:
        return None

def list_folders(directory):
    folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
    return folders

def get_comic_series_info(settings, metron, folders, directory):

    for folder in folders:

        #Getting the Metron ID
        id = get_volume_id(folder)

        if id is not None:
            path = os.path.join(directory,folder)
            last_modified_folder = os.path.getmtime(path)
            
            if float(last_modified_folder) > float(settings.last_run):

                #Retrieve Series Information
                series = Series(metron.series(id))
                if series != None:

                    #Creating a new name for the folder
                    newFolder = f"{series.name} ({series.year}) {'{'}mt-{series.comicid}{'}'}"
                    newFolder = newFolder.replace(":","_")

                    #Checking if the folder names are the same
                    if newFolder != folder:
                        print("Renamed:", newFolder )
                        newPath = os.path.join(directory,newFolder)
                        rename_folder(path, newPath)

                    #Save the series.json File
                    series.saveSeries(directory, newFolder)
            else:
                print('- No Changes: ', folder)
        else:
            print("X No Metron ID Found: ", folder)

            

def main():
    directory = input("Enter the path of the directory: ")
    data = read_settings()

    settings = Settings(data.get('username',''), data.get('password',''), data.get('last_run',0))

    metron = Metron(settings.username, settings.password)


    if os.path.exists(directory):
        folders = list_folders(directory)
        if folders:
            get_comic_series_info(settings, metron, folders, directory)
        else:
            print("No folders found in the directory.")
        #save_settings()
    else:
        print("Directory not found.")

    
        
#
if __name__ == "__main__":
    main()