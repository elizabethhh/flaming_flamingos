import tokens
import tweepy



auth = tweepy.OAuthHandler(tokens.api_key, tokens.api_secret_key)
print("Go to the following URL to login")
print(auth.get_authorization_url())
verify = input("Enter verification code")
token = auth.get_access_token(verifier=verify)
mycreds = {
        'consumer_key': tokens.api_key,
        'consumer_secret': tokens.api_secret_key,
        'access_token': token[0],
        'access_token_secret': token[1]
}
t_auth = tweepy.OAuthHandler(
        consumer_key=mycreds['consumer_key'],
        consumer_secret=mycreds['consumer_secret']
)
t_auth.set_access_token(
        mycreds['access_token'],
        mycreds['access_token_secret']
)
api = tweepy.API(t_auth)


ranked_tweets = []
location_markers = ['st.', 'st', 'av', 'avenue', 'road', 'park', 'lane', 'ln', 'l.n.', 'street', 'corner']
time_markers = ["hrs", "a.m", "a.m.","m.m", "p.m.", "am", "pm", "morning", "evening", "afternoon", "now"]
date_markers = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"
                "today", "tomorrow", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
police_markers = ["police", "feds", "blue", "cops"]


#followers = api.followers()

#Live streaming
class MaxListener(tweepy.StreamListener):
    def on_data(self, raw_data):
        self.process_data(raw_data)
        return True
    def process_data(self, raw_data):
        """FILL IN HERE
        """
        iden = raw_data[52:71] #id num
        print(iden)

    def on_error(self, status_code):
        if status_code == 420:
            return False

class MaxStream():
    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth,listener=listener)
    def start(self, keyword_list):
        self.stream.filter(track=keyword_list,is_async=True)

listener = MaxListener()

auth = tweepy.OAuthHandler(tokens.api_key,tokens.api_secret_key)
auth.set_access_token(tokens.access_token_key,tokens.access_token_secret)

stream = MaxStream(auth, listener)
responses = stream.start("python")


for tweet in responses:
    xyz = tweet._json
    iden = xyz['id']
    score = 0
    tweet_content = xyz['text'].split()  # separate tweet content by whitespace
    for word in tweet_content:
        if word.lower() in location_markers:
            score += 1
        if word.lower() in time_markers:
            score += 1
        if word.lower() in date_markers:
            score += 1
        if word.lower() in police_markers:
            score += 1


    #engagement_and_informative_score = ((xyz['favourites_count'] / xyz["followers_count"]) + (score / 4)) / 2
    #score = engagement_and_informative_score
    ranked_tweets.append((iden, score))

ranked_tweets.sort(key=lambda x: x[1], reverse=True)
counter = 0

for i in range(10):
    print(ranked_tweets[i][0])
    try:
        api.retweet(id=ranked_tweets[i][0])
    except:
        continue


#only take tweets relevant from the last half hour
    #extract the tweet id to be the variable name
    #check if all the parameters are present, if they are add them to the relevant
    #member function then update score by one
    #add the tweet_class to our tweets list
    #rank tweet class by score, highest score to lowest
    #every 5 minutes, grab the most relevant tweet, retweet it then remove it from our list
    #update list every half hour
    #before retweeting, have a bad word list, and if any word in the tweet is in the bad words then remove that tweet
    #from our list, if the tweet is clean retweet it

