from google.cloud import storage
from google.auth import compute_engine
import os
import json


class GCPDownloaderLocal:
    def __init__(self):
        self.__key_location_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'key'))
        with open(self.__key_location_file + '/key_location.json', 'r') as json_file:
            self.__data = json.loads(json_file.read())
            self.__key_path = self.__data['data']['key_location']
        self.__storage_client = storage.Client.from_service_account_json(self.__key_path)

    def getData(self, project, project_name, folder_name, file_name):
        bucket = self.__storage_client.get_bucket(project_name)
        blob = bucket.blob(folder_name + '/' + file_name)
        content = blob.download_as_string()
        return content


class GCPDownloaderCloud:

    def getData(self, project, project_name, folder_name, file_name):
        credentials = compute_engine.Credentials()
        storage_client = storage.Client(credentials=credentials, project=project)
        bucket = storage_client.get_bucket(project_name)
        blob = bucket.blob(folder_name + '/' + file_name)
        content = blob.download_as_string()
        return content


if __name__ == '__main__':
    project_name = 'dash-example-265811.appspot.com'
    folder_name = 'data'
    file_name = 'data.csv'
    GCP = GCPDownloaderLocal()
    content = GCP.getData(project_name, folder_name, file_name)