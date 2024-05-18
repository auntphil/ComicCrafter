import json

def create_series_file(data, directory, folder):
    series = {
        "metadata": data
    }
    series_string = json.dumps(series,indent=4)

    with open(directory + '/' + folder + '/series.json', 'w') as json_file:
        json_file.write(series_string)