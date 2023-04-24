import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
from textblob import TextBlob

st.set_page_config(page_title="Twitter Sentiment Analysis App")

# Set page title and layout
st.title("Twitter Sentiment Analysis App")
st.sidebar.header("User Input")
st.sidebar.write("Enter the keyword(s) to search for on Twitter:")

# take user input for the search query
search_query = st.sidebar.text_input(label="", value="", max_chars=None, key=None, type='default')

# create the query string with lang:en filter
query = search_query + " lang:en"

# create a function to perform sentiment analysis
def analyze_sentiment():
    tweets =[]
    limit = 10 # limit the number of tweets returned
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if len(tweets) == limit:
            break
        else:
            tweets.append([tweet.date, tweet.user.username, tweet.content])
    
    df= pd.DataFrame(tweets, columns=['Date','User','Tweet'])

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

    # return the sentiment analysis results
    return sentiment_counts

# create a function to display the sentiment analysis results
def display_results(results):
    st.subheader("Sentiment Analysis Results:")
    st.write(results)
    # display a summary of the sentiment analysis results
    if len(results) > 0:
        sentiment = results['Sentiment'][0]
        if sentiment > 0:
            st.write("Overall sentiment: Positive")
        elif sentiment < 0:
            st.write("Overall sentiment: Negative")
        else:
            st.write("Overall sentiment: Neutral")
    else:
        st.write("No tweets found for the entered keyword(s).")

# add a submit button to trigger sentiment analysis
submit = st.sidebar.button("Submit")

# perform sentiment analysis and display the results when the submit button is clicked
if submit:
    results = analyze_sentiment()
    display_results(results)
