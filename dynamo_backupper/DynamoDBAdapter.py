import boto3

class DynamoDBAdapter:
    def __init__(self, region_name):
        self.region_name = region_name
        self.dynamo_db = boto3.resource('dynamodb', region_name=self.region_name)

    def scan(self, table_name):
        return self.dynamo_db.Table(table_name).scan()