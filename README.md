#Sentiment Analysis on Twitter

###Summary

Given a sample data, filtered with keywords: 'job', 'jobs', and 'work', collected from Twitter API Version 1.1, this application performed a sentiment analysis using the lexical affinity approach. As a result, the statistic of the sentiment score of each state in the U.S. and overall statistic, and the ten most frequently occurred hash tags involved were returned.

This application takes three arguments from the command line:

1. _us-states.json_ : Containing a JSON object which holds the names of the states in the U.S. as the keys and the coordinates of a list of vertices around the states as the respective values.

2. _AFINN-111.txt_: The sentiment dictionary distributed under [Open Database License (ODbL) v1.0](http://www.opendatacommons.org/licenses/odbl/1.0/) for the sentiment scores computation.

3. job.txt: A text file containing the raw data collected from Twitter API.

Note: Only states from which at least one tweet emitted would appear in the result.
