import sys
import io
import pandas as pd
from datetime import date
from dynamo_backupper.DynamoDBAdapter import DynamoDBAdapter
from dynamo_backupper.GoogleAPIAdapter import GoogleAPIAdapter

# Args are aws-region, dynamodb table name, and google drive folder to upload to
def main(argv):
    # Create the adapter instance
    db_adapter= DynamoDBAdapter(argv[0])

    # Try to fetch data, if it blows up let it so the stack get logged into logs
    data = db_adapter.scan(argv[1])

    # Create Stream 
    file_stream = io.StringIO()
    pd.DataFrame(data['Items']).to_csv(file_stream)

    google_api_adapter = GoogleAPIAdapter()

    folder_id = google_api_adapter.find_folder_id(argv[2])
    google_api_adapter.upload_csv_under_folder(str(date.today()), file_stream, folder_id)

if __name__ == "__main__":
   main(sys.argv[1:])