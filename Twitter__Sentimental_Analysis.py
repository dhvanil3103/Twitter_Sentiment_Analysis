import snscrape.modules.twitter as sntwitter
import pandas as pd
from textblob import TextBlob
pd.set_option('display.max_colwidth', None)

# take user input for the search query
search_query = input("Enter the Twitter search query: ")

# create the query string with lang:en filter
query = search_query + " lang:en"

tweets =[]
limit = 1
for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.date, tweet.user.username, tweet.content])

df= pd.DataFrame(tweets, columns=['Date','User','Tweet'])
print(df)

# perform sentimental analysis on the tweets
sentiments = []
for tweet in df['Tweet']:
    blob = TextBlob(tweet)
    sentiment = blob.sentiment.polarity
    sentiments.append(sentiment)

# add the sentiments to the dataframe
df['Sentiment'] = sentiments

# group the tweets by sentiment and count the number of tweets in each group
sentiment_counts = df.groupby('Sentiment').size().reset_index(name='Count')

# calculate the percentage of tweets in each sentiment group
total_tweets = sentiment_counts['Count'].sum()
sentiment_counts['Percentage'] = sentiment_counts['Count'] / total_tweets * 100

print(sentiment_counts)
