import boto3 

class ComprehendHandler:

    def __init__(self, accessKey, secretAccessKey):
        self.client = boto3.client('comprehend',
                       aws_access_key_id=accessKey,
                       aws_secret_access_key=secretAccessKey, 
                       region_name='us-west-2')

    def detectSentiment(self, message):
        sentiment = self.client.detect_sentiment(Text=message, LanguageCode='pt')
        return sentiment

    def close(self):
        self.client = None
