import requests, json
from datetime import datetime as dt
import time

class Metron ():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.baseUrl = "https://metron.cloud/api/"
        self.apiLimiterTime = 0
        self.apiLimiterCounter = 0
    
    #API Limit Check
    def apiLimiter(self):
        if self.apiLimiterTime == 0:
            self.apiLimiterTime = int(time.time())

        if (int(time.time()) - self.apiLimiterTime) < 60:
            if self.apiLimiterCounter > 29:
                time.sleep(61 - (int(time.time()) - self.apiLimiterTime))
                self.apiLimiterCounter = 1
            else:
                self.apiLimiterCounter+=1
        else:
            self.apiLimiterTime = int(time.time())
            self.apiLimiterCounter = 1

    def series(self, id):
        try:
            session = requests.Session()
            session.auth = (self.username, self.password)

            self.apiLimiter()
            response = session.get(f"{self.baseUrl}series/{id}/")

            #Checking if the request was successful
            if(response.status_code != 200):
                return None
            
            series = response.json()
        
            self.apiLimiter()
            response = session.get(f"{self.baseUrl}series/{id}/issue_list/")

            #Checking if the request was successful
            if(response.status_code != 200):
                series['issues'] = {}
            else:
                series['issues'] = response.json()
            
            #Loading Response into Dictionary
            return series

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
        
class Series:
    def __init__(self, series):
        if series == None:
            return None

        self.type = ''
        self.publisher = f"{series['publisher']['name']}"
        self.imprint = ''
        self.name = f"{series['name']}"
        self.comicid = series['id']
        self.year = series['year_began']
        self.year_end = series['year_end']
        self.description_text = f"{series['desc']}"
        self.description_formatted = ''
        self.volume = f"{series['year_began']}"
        self.booktype = f"{series['series_type']['name']}"
        self.collects = ''
        self.comic_image = ''
        self.total_issues = series['issue_count']
        self.publication_run = f"{series['year_began']}"
        self.status = 'Continuing'
        self.issues = series["issues"]["results"]

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