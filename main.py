import requests
import requests.auth
import praw
from requests import Session
import time
import configparser
import random

class Gauntlet(object):
    def __init__(self, *args, **kwargs):
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')
        return super(Gauntlet, self).__init__(*args, **kwargs)

    def getAuthToken(self):
        session = Session()
        self.reddit = praw.Reddit(client_id=self.config['PARAMETERS']['Client_ID'],
                     client_secret=self.config['PARAMETERS']['secret'],
                     password=self.config['PARAMETERS']['Password'],
                     requestor_kwargs={'session': session},  # pass Session
                     user_agent='Infinity Gauntlet test app v0.1',
                     username=self.config['PARAMETERS']['Username'])
        test = ""

    def getUsersFromSubreddit(self):
        users = []  
        for submission in self.reddit.subreddit(self.config['PARAMETERS']['Subreddit']).new(limit=2048):
            if(hasattr(submission.author,'name')):
                users.append(submission.author.name)
            for user in self.getUsersFromSubmission(submission):
                users.append(user)
        users = tuple(users)
        users = list(set(users))
        return users

    def getUsersFromSubmission(self,submissionID):
        users = []
        for TLC in submissionID.comments:
            if(hasattr(TLC,'author')):
                if(hasattr(TLC.author,'name')):
                    users.append(TLC.author.name)
            if(hasattr(TLC,'replies')):
                for user in self.getUsersFromCommentForest(TLC.replies):
                    users.append(user)
        return users
    def getUsersFromCommentForest(self,forest):
        users = []
        forest.replace_more(limit=None)
        for comment in forest.list():
            if(hasattr(comment,'author')):
                if(hasattr(comment.author,'name')):
                    users.append(comment.author.name)
        return users

    def writeOutVictims(self,usernamelist):
        with(open('victims.txt','w')) as File:
             for user in usernamelist:
                 File.write(user)
                 File.write('\n')
    def readInVictims(self):
        with(open('victims.txt','r')) as File:
            content = File.readlines()
            content = [x.strip() for x in content] 
        return content
    def Snap(self,subreddit,user_list):
        for user in user_list:
            #50% chance of ban for anyone on the list
            if(random.uniform(0, 1) < 0.5):
                self.reddit.subreddit(subreddit).banned.add(user, ban_reason=self.config['PARAMETERS']['Message'])
                time.sleep(1)#Reddit API rate limit, 1 user per second
 
def main():    
    ThanosRightHand = Gauntlet()
    ThanosRightHand.getAuthToken()
    users = ThanosRightHand.getUsersFromSubreddit()
    ThanosRightHand.writeOutVictims(users)
    print(len(users))
    #When you're ready to commence banning, uncomment these lines.
    #users = ThanosRightHand.readInVictims()
    #ThanosRightHand.Snap(subreddit,users)
    pass

if __name__ == "__main__":
    main()

    