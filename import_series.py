import os, re, json, mokkari, sys
from import_issues import import_issues
from file_rename import rename_folder
from create_series import create_series_file
from datetime import datetime as dt

class Settings:
    def __init__(self, username, password, last_run):
        self.username = username
        self.password = password
        self.last_run = last_run

class Series:
    def __init__(self, data):
        self.type = ''
        self.publisher = data.publisher.name
        self.imprint = ''
        self.name = data.name
        self.comicid = data.id
        self.year = f"{data.year_began}"
        self.description_text = data.desc
        self.description_formatted = ''
        self.volume = f"{data.year_began}"
        self.booktype = data.series_type.name
        self.collects = ''
        self.comic_image = ''
        self.total_issues = data.issue_count
        self.publication_run = f"{data.year_began}"
        self.status = 'Continuing'

    def set_publication_run(self, start, end):
        if dt.now().year > end:
            #If the Current Year is later than the Series End Year
            self.status = "Ended"
            if start == end:
                self.publication_run = f"{start}"
            else:
                self.publication_run = f"{start} - {end}"

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
                try:
                    series = metron.series(id)
                    series_file = Series(series)
                    series_file.set_publication_run(series.year_began, series.year_end)
                except mokkari.exceptions.ApiError as e:
                    print(e)
                    series = None
                except:
                    print("Error gettings series")
                    series = None

                if series != None:
                    #Creating a new name for the folder
                    newFolder = f"{series.name} ({series.year_began}) {'{'}mt-{series.id}{'}'}"
                    newFolder = newFolder.replace(":","_")

                    #Checking if the folder names are the same
                    if newFolder != folder:
                        print("Renamed:", newFolder )
                        newPath = os.path.join(directory,newFolder)
                        rename_folder(path, newPath)
                    
                    #import_issues(data)
    #
                    create_series_file(series_file.__dict__, directory, newFolder)
            else:
                print('- No Changes: ', folder)
        else:
            print("X No Metron ID Found: ", folder)

            

def main():
    directory = input("Enter the path of the directory: ")
    data = read_settings()

    settings = Settings(data.get('username',''), data.get('password',''), data.get('last_run',0))

    metron = mokkari.api(settings.username, settings.password)


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