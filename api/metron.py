import requests, json
from datetime import datetime as dt

class Metron ():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.baseUrl = "https://metron.cloud/api/"

    def series(self, id):
        try:
            session = requests.Session()
            session.auth = (self.username, self.password)
            response = session.get(f"{self.baseUrl}series/{id}/")

            #Checking if the request was successful
            if(response.status_code != 200):
                return None
            
            #Loading Response into Dictionary
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
        
        
class Series:
    def __init__(self, data):
        if data == None:
            return None

        self.type = ''
        self.publisher = f"{data['publisher']['name']}"
        self.imprint = ''
        self.name = f"{data['name']}"
        self.comicid = data['id']
        self.year = data['year_began']
        self.year_end = data['year_end']
        self.description_text = f"{data['desc']}"
        self.description_formatted = ''
        self.volume = f"{data['year_began']}"
        self.booktype = f"{data['series_type']['name']}"
        self.collects = ''
        self.comic_image = ''
        self.total_issues = data['issue_count']
        self.publication_run = f"{data['year_began']}"
        self.status = 'Continuing'

        if dt.now().year > self.year_end:
            #If the Current Year is later than the Series End Year
            self.status = "Ended"
            if self.year == self.year_end:
                self.publication_run = f"{self.year}"
            else:
                self.publication_run = f"{self.year} - {self.year_end}"
    
    #Creates the series.json file
    def saveSeries(self, directory, folder):
        series = {
            "metadata": self.__dict__
        }

        series_string = json.dumps(series,indent=4)

        with open(directory + '/' + folder + '/series.json', 'w') as json_file:
            json_file.write(series_string)