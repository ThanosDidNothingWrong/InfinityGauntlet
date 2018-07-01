import requests
import requests.auth
import praw
from requests import Session
import time
import configparser
import random

class Gauntlet(object):
    """Interface for mass-banning half the participating users in a subreddit."""

    def __init__(self, *args, **kwargs):
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')
        return super(Gauntlet, self).__init__(*args, **kwargs)

    def getAuthToken(self):
        #If this is failing, you need to register your app, and update settings.ini.
        #Always be sure to never commit a copy of settings.ini with your actual password.  
        session = Session()
        self.reddit = praw.Reddit(client_id=self.config['PARAMETERS']['Client_ID'],
                     client_secret=self.config['PARAMETERS']['secret'],
                     password=self.config['PARAMETERS']['Password'],
                     requestor_kwargs={'session': session},  # pass Session
                     user_agent='Infinity Gauntlet test app v0.1',
                     username=self.config['PARAMETERS']['Username'])

    def getUsersFromSubreddit(self,subredditName):
        #TODO:  This assumes just one subreddit, which is set in the settings.ini file
        #Consider changing this to pull from all of the top subreddits.
        users = [] 
        i = 1
        for submission in self.reddit.subreddit(subredditName).new(limit=1000):
            users = self.addUserToVictimList(submission,users)
            self.getUsersFromSubmission(submission,users)
            print(repr(i) + " submissions parsed.  " + repr(len(users)) + " unique users found")
            i += 1
        for submission in self.reddit.subreddit(subredditName).top(limit=1000):
            users = self.addUserToVictimList(submission,users)
            self.getUsersFromSubmission(submission,users)
            print(repr(i) + " submissions parsed.  " + repr(len(users)) + " unique users found")
            i += 1
        self.writeOutVictims(users,subredditName + ".txt")
        return users

    def addUserToVictimList(self, id,users):
        if(hasattr(id,'author')):
            if(hasattr(id.author,'name')):
                if(id.author.name not in users):
                    users.append(id.author.name)
        return users

    def getUsersFromSubmission(self,submissionID,users):
        for TLC in submissionID.comments:
            self.addUserToVictimList(TLC,users)
            if(hasattr(TLC,'replies')):
                users = self.getUsersFromCommentForest(TLC.replies,users)
        return users

    def getUsersFromCommentForest(self,forest,users):
        forest.replace_more(limit=None)
        for comment in forest.list():
            users = self.addUserToVictimList(comment,users)
        return users

    def writeOutVictims(self,usernamelist, filename):
        with(open(filename,'w')) as File:
             for user in usernamelist:
                 File.write(user)
                 File.write('\n')
    def readInVictims(self,filename):
        with(open(filename,'r')) as File:
            content = File.readlines()
            content = [x.strip() for x in content] 
        return content

    def Snap(self,subreddit,user_list):
        #TODO:  Save out a list of people who have avoided the purge so this can be done incrementally.
        for user in user_list:
            #50% chance of ban for anyone on the list
            if(random.uniform(0, 1) < 0.5):
                #self.reddit.subreddit(subreddit).banned.add(user, ban_reason=self.config['PARAMETERS']['Message'])
                print(user + " Was banned")
                time.sleep(1)#Reddit API rate limit, 1 user per second
            else:
                print(user + " was not banned")

 
def main():    
    ThanosRightHand = Gauntlet()
    ThanosRightHand.getAuthToken()
    users = ThanosRightHand.getUsersFromSubreddit(ThanosRightHand.config['PARAMETERS']['subreddit'])
    ThanosRightHand.writeOutVictims(users)
    print(len(users))
    #When you're ready to commence banning, uncomment these lines.
    #users = ThanosRightHand.readInVictims()
    #ThanosRightHand.Snap(subreddit,users)
    pass

if __name__ == "__main__":
    main()

    