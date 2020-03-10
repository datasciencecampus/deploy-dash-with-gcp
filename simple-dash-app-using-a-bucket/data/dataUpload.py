from google.cloud import storage
import os
import json


class GCPUploader:
    def __init__(self):
        self.__key_location_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'key'))
        with open(self.__key_location_file + '/key_location.json', 'r') as json_file:
            self.__data = json.loads(json_file.read())
            self.__key_path = self.__data['data']['key_location']
        self.__storage_client = storage.Client.from_service_account_json(self.__key_path)

    def upload_blob(self, project_name, df, destination_blob_name):
        """Uploads a file to the bucket."""

        bucket = self.__storage_client.bucket(project_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(df.to_csv(), 'text/csv')


if __name__ == '__main__':

    df = create_data_frame()
    project_name = <PROJECT-NAME>
    destination_blob_name = <BLOB-NAME>
    upload = GCPUploader()
    upload.upload_blob(project_name, df, destination_blob_name)