import boto3
import boto3.session

class SessionProvider: 
    
    def __init__(self):
        self.region_name = 'us-west-2'
        self.profile_name = 'devops-batch7'
        self.session = boto3.session.Session(profile_name=self.profile_name, region_name=self.region_name)
        
    def get_session(self):
        return self.session