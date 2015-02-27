import sys
import json
import fileinput
import pandas as pd
import numpy as np

# A dictionary having the names of the states as keys
# and a list of coordinates of vertices of the subscribing polygon
# as the respective value.
statesVertices = {}
# The sentiment dictionary.
sentimentDF = pd.DataFrame()
# The set of tweets that were from the U.S. and had nonempty text field.
tweetsDF = pd.DataFrame()
# List of nonempty hashtages involved in the tweets.
hashtags = []

"""
sent_score() computes the total sentiment score from a specified list of terms.

@param split_tweet A list of terms whose sentiment scores are to be summed.
@return total The total sentiment score from the specified list of terms.
"""
def sent_score(split_tweet): 
    total = 0 # Score of a tweet.
    n = len(split_tweet)
	
    # Searches for the 3-word terms and their negations.
    span = 3
    start = 0
    while start <= n-span :
	    space = ' '
	    seq = (split_tweet[start:start+span])
	    phrase = space.join(seq)
	    if phrase in list(sentimentDF.term[sentimentDF.numWords==3]):
		    if start > 0 and split_tweet[start-1]=="not":
			    total -= int(sentimentDF.score[sentimentDF.term==phrase])
			    del split_tweet[start-1:start+span]
			    n = len(split_tweet)
			    start -= 2
		    else:
			    total += int(sentimentDF.score[sentimentDF.term==phrase])
			    del split_tweet[start:start+span]
			    n = len(split_tweet)
			    start -= 1
	    else:
		    start += 1		
    
	# Searches for the 2-word terms and their negations.
    span = 2
    start = 0
    while start <= n-span :
	    space = ' '
	    seq = (split_tweet[start:start+span])
	    phrase = space.join(seq)
	    if phrase in list(sentimentDF.term[sentimentDF.numWords==2]):
		    if start > 0 and split_tweet[start-1]=="not":
			    total -= int(sentimentDF.score[sentimentDF.term==phrase])
			    del split_tweet[start-1:start+span]
			    n = len(split_tweet)
			    start -= 2
		    else:
			    total += int(sentimentDF.score[sentimentDF.term==phrase])
			    del split_tweet[start:start+span]
			    n = len(split_tweet)
			    start -= 1
	    else:
		    start += 1
			
	# Searches for the 1-word terms and their negations.
    span = 1
    start = 0
    while start <= n-span :
	    space = ' '
	    seq = (split_tweet[start:start+span])
	    phrase = space.join(seq)
	    if phrase in list(sentimentDF.term[sentimentDF.numWords==1]):
		    if start > 0 and split_tweet[start-1]=="not":
			    total -= int(sentimentDF.score[sentimentDF.term==phrase])
			    del split_tweet[start-1:start+span]
			    n = len(split_tweet)
			    start -= 2
		    else:
			    total += int(sentimentDF.score[sentimentDF.term==phrase])
			    del split_tweet[start:start+span]
			    n = len(split_tweet)
			    start -= 1
	    else:
		    start += 1
    return total

"""
scrub_text() removes all the punctuations and extra spaces in the specified text.
@param text The text whose punctuations and extra spaces are to be removed.
@return split_text A list containing only the words in the specified text.
"""
def scrub_text(text):
    value1 = text.lower()
    value2 = value1.replace('!',' ')
    value3 = value2.replace('?',' ')
    value4 = value3.replace(',',' ')
    value5 = value4.replace('.',' ')
    value6 = value5.replace(':',' ')
    value7 = value6.replace(';',' ')
    value8 = value7.replace('-',' ')
    clean_text = value8.strip()
    split_text1 = clean_text.split(' ')
    split_text = []
    for x in split_text1:
        if not x == '':
            split_text.append(x)
    return split_text           	
	
"""
in_state() determines which state the specified point locates.

@param pt The specified point.
@return The name of the state in which the specified point locates 
if a state is detected and `undetermined` otherwise.
"""
def in_state(pt):
    x = pt[0]
    y = pt[1]

    for key in statesVertices.keys():
	    xcoords = [] # List of x-coordinates of the vertices
	    ycoords= [] # List of y-coordinates of the vertices
	    for vertex in statesVertices[key]:
		    xcoords.append(vertex[0])
		    ycoords.append(vertex[1])
	    n = len(xcoords)
	    l = n-1
	    for k in range(n):
		    if ycoords[k]<y and ycoords[l]>=y or ycoords[l]<y and ycoords[k]>=y:
			    z = xcoords[k] + (y-ycoords[k])*(xcoords[l]-xcoords[k])/(ycoords[l]-ycoords[l]-ycoords[k])
			    if z < x:
				    return key
		    l=k   
    return 'undetermined'

"""
center() computes the coordinates of the center of the convex hull 
having the specified set of vertices.

@param pts The specified list of coordinates of vertices.
@return Coordinates of the center of the convex hull.
"""
def center(pts):
    if len(pts) < 4:
        return pts
    p1 = pts[0]
    p2 = pts[2]
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    
    return [(x1+x2)/2, (y1+y2)/2] 

"""
targetTweets() reads the tweets, filters the tweets that are from the U.S. 
and extracts the locations in coordinates, contents, and hashtags.

@param s The file stream carrying the tweets. 
"""
def targetTweets(s):
    tweets = s.readlines()
    states = []
    text = []
    for line in tweets:
	    tweet = json.loads(line)
	    if 'text' in tweet.keys() and 'place' in tweet.keys() and \
        not tweet['place'] == None and tweet['place'] ['country_code'] == 'US':
		    # A list of the vertices of the box
		    coords = tweet['place'] ['bounding_box']['coordinates'][0]
		    theState = in_state(center(coords))		
		    if not theState == 'undetermined':
			    states.append(theState)
			    value = tweet['text'].encode('utf-8')
			    text.append(value)
	    if 'entities' in tweet.keys() and len(tweet['entities']['hashtags'])>0:
		    htags = tweet['entities']['hashtags']
		    for htag in htags:
			    ht = htag['text'].encode('utf-8')
			    hashtags.append(ht.lower())
    tweetsDF["state"] = states
    tweetsDF["text"] = text
   
"""
sentStat() performs a statistic on the sentiment scores on the tweets 
and displays the result.
"""
def sentStat():
    tweetsDF["score"] = tweetsDF["text"].apply(lambda x: sent_score(scrub_text(x)))
    tweetsDF.drop("text",inplace=True,axis=1)
    stat = pd.DataFrame(tweetsDF.groupby(["state"]).agg(['count','mean','std']))
    print "\n\nSTATISTIC OF SENTIMENT SCORE BY STATE:"
    print stat
    print "\n\n"
    print stat.describe()

"""
tagStat() counts the occurrences of each hash tags and displays
the ten most frequently occurred hash tags..
"""	
def tagStat():
    tags = pd.DataFrame()
    tags["hashtag"] = hashtags
    tags["count"] = 1
    tags = tags.groupby("hashtag").count()
    tags = tags.sort("count", ascending=False)
    print "\n\nTEN MOST FREQUENTLY OCCURRED HASH TAGS:"
    print tags[0:10]

"""
sentDict() extracts the sentiment terms and their scores from 
the specified file and counts the number of words in each term.

@param s The specified file.
"""
def sentDict(s):
    sfile = s.readlines()
    terms = []
    scores = []
    for line in sfile:
	    term, score  = line.split("\t")
	    terms.append(str(term))
	    scores.append(int(score))
    sentimentDF["term"] = terms
    sentimentDF["score"] = scores
    sentimentDF["numWords"] =  sentimentDF["term"].apply(lambda x: x.count(" ") + 1)

"""
parseStates() extracts the name of the states and the list of coordinates 
of vertices of the subscribing polygon from the json object in the specified
 file.
 
 @param s The specified file.
"""
def parseStates(s):    
    states = s.read()
    statesJ = json.loads(states)
    for i in range(len(statesJ['features'])):
	    statesVertices[statesJ['features'][i]["properties"]["name"]] = \
	    statesJ['features'][i]["geometry"]["coordinates"][0][0]
    
def main():
    state_file = open(sys.argv[1], "r")
    sent_file = open(sys.argv[2], "r")
    tweet_file = open(sys.argv[3],"r")
    parseStates(state_file)
    sentDict(sent_file)
    targetTweets(tweet_file)
    sentStat()
    tagStat()
    state_file.close()
    sent_file.close()
    tweet_file.close()

if __name__ == '__main__':
    main()
