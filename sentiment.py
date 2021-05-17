import re
import os
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

 
class TwitterClient(object):
    '''
    Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter API
        consumer_key = os.getenv("CONSUMER_KEY")
        consumer_secret = os.getenv("CONSUMER_SECRET")
        access_token = os.getenv("ACCESS_TOKEN")
        access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        '''
        Function to clean tweet text by replacing emoticons with their meanings; removing stop words links, special characters
        using simple regex statements.
        '''
        
        lis= ' '.join(re.sub("( me | my | myself | we | our | ours | ourselves | you | your | yours | yourself |yourselves | he | him | his | himself | she | her | hers | herself | it | its | itself | they | them | their | theirs | themselves | what | which | who | whom | this | that | these | those | am | is | are | was | were | be | been | being | have | has | had | having | do | does | did | doing | an | the | a | and | but | if | or | because | as | until | while | of | at | by | for | with | about | against | between | into | through | during | before | after | above | below | to | from | up | down | in | out | on | off | over | under | again | further | then | once | here | there | when | where | why | how | all | any | both | each | few | more | most | other | some | such | no | nor | only | own | same | so | than | too | very | can | will | just | don | should | now | ain | aren | couldn | didn | doesn | hadn | hasn | haven | isn | ma | mightn | mustn | needn | shan | shouldn | wasn | weren | won | wouldn | I |RT )"," ",tweet).split())
        lis.lower()
        lis=' '.join(re.sub(":\) |:-\) | \^.\^ |\^_\^ | :p | :-p | : \)"," happy ",lis).split())
        lis=' '.join(re.sub(":\( |:-\( | :/ "," sad ",lis).split())
        lis=' '.join(re.sub(" xd | :d |:-d | x-d"," funny ",lis).split())
        lis=' '.join(re.sub("\*_\* "," amazing ",lis).split())
        lis=' '.join(re.sub("-.- |-_- | x-\( | x\( "," angry ",lis).split())
        

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", lis).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Function to classify sentiment of passed tweet
        
        '''
        # create TextBlob object of passed tweet text
        #print(self.clean_tweet(tweet),"\n")
        analysis = TextBlob(self.clean_tweet(tweet))
        
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'  
 
    def get_tweets(self, query, count = 1000):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
        fetched_tweets=[]
        try:
            # call twitter api to fetch tweets
            fetched = self.api.search(q = query, count = count)
            # filter tweets with english script
            for tweet in fetched:
                if tweet.lang == "en":
                    fetched_tweets.append(tweet)
 
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
           
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
 
def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    keyword=input("Enter the word to fetch the tweets for: ")
    tweets = api.get_tweets(query = keyword, count = 1000)
    
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # picking neutral tweets from tweets
    neutral=[tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
    count =1
    # printing positive tweets
    
    print("\n\nPositive tweets:")
    for tweet in ptweets[:len(ptweets)]:
        print(count,") ",tweet['text'])
        count=count+1
    count=1    
    # printing negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:len(ntweets)]:
        print(count,") ",tweet['text'])
        count=count+1
    count=1 
    # printing negative tweets
    print("\n\nNeutral tweets:")
    for tweet in neutral[:len(neutral)]:
        print(count,") ",tweet['text'])
        count=count+1
if __name__ == "__main__":
    # calling main function
    main()