import os

import pandas as pd
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)
#comment

class Database:
    def __init__(self, language='pl'):
        self.areas = []
        self.api_key = os.environ['DBW_API_KEY']
        self.language = language
        self.header = {'accept': 'application/json', 'X-ClientId': self.api_key}

    def get_areas(self):
        request_url = f'https://api-dbw.stat.gov.pl/api/1.1.0/area/area-area?lang={self.language}'
        request = requests.get(request_url, headers=self.header)
        self.areas = {area['id']: Area(area['nazwa'], area['id']) for area in request.json()}
    
    def list_areas(self):
        for area in self.areas['nazwa'].values:
            print(area)

    def retrieve_area(self, area_id):
        return self.areas[area_id]


class Area(Database):
    def __init__(self, name, id):
        super().__init__()
        self.name = name
        self.id = id

    def get_variables(self):
        request_url = f'https://api-dbw.stat.gov.pl/api/1.1.0/area/area-variable?id-obszaru={self.id}&lang={self.language}'
        request = requests.get(request_url, headers=self.header)
        variables = request.json()
        print(variables)

    def __repr__(self):
        return f"{self.id}. {self.name}"


class Variable:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        

if __name__ == '__main__':
    database = Database()
    database.get_areas()
    area = database.retrieve_area(16)
    area.get_variables()

