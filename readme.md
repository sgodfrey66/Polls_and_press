# Analyzing the relationship between press coverage and polling performance

### Stephen Godfrey, DSI-CC7-San Francisco

### Problem Statement

Explore and quantify the relationship between press coverage and polling performance.



### Executive Summary

Candidate polling is an important part of the political campaign process.  Poll results are closely watched by voters, journalists and, of course, candidates and their campaigns.  An increases in poll standings can help a campaign build momentum, solidy support and spur fundraising.  Decreases can have the opposite effects. Polls are particularly important in races with many candidates, as each participant struggles to differentiate from the pack.  Poll numbers can provide one metric by which candidates argue that they are achieving such differentiation.   As this is being written in May 2019, the U.S. is in the early stages of the 2020 presidential election and there are already some 20 Democratic candidates vying to earn their party's nomination and face the likely Republican nominee, Donald Trump.  Understanding poll drivers is of keen interest to these candidates, their supporters and opponents and to neutral observers.

One driver is media reporting and this analysis employs quantitative techniques to explore and model the relationship between press coverage and poll results.  To do so, I study the 2016 Republican presidential primary contest since it has similarities to today's Democratic race and might be a source of useful insights.  The approach is to build a data set that consists of poll results and key press-coverage metrics and themes from 2015 and 2016, a period in which the primary election process trimmed the a field consisting of many candidates down to one winner, Donald Trump.

The steps in the analysis are to use the data to make both qualitative and quantitative observations.  Quantitative observations are made by constructing models that use press coverage variables to predict future poll performance. 


### Conclusions and Recommendations



### Notebooks

* [Poll results](code/Poll_data_2016.ipynb)
* [Press coverage](code/Google_BigQuery.ipynb)
* [Data construction](code/Data_construction.ipynb)
* [Data modeling](code/Data_modeling.ipynb)



### Data

#### Data sources:

To conduct this analysis both polling press-coverage data are required.  These were collected from two different sources, [FiveThirtyEight](https://fivethirtyeight.com/) and the Global Data on Events, Language and Tone or [GDELT](https://www.gdeltproject.org/) project.  

FiveThirtyEight is a analytical service with a popular website that provides quantitative and statistical analysis of politics, sports, science and health, economics and culture.  For this project, polling data from the 2015/2016 Republican presidential primary were obtained from a specific FiveThirtyEight [page](https://projects.fivethirtyeight.com/election-2016/national-primary-polls/republican/). These data covered 670 polls between Jan 25, 2015 and May 3, 2016 and included results for 11 candidates (Donald Trump, John Kasich, Ted Cruz, Marco Rubio, Ben Carson, Jeb Bush, Chris Christie, Carly Fiorina, Rick Santorum, Rand Paul and Mike Huckabee).

GDELT is supported by Google Jigsaw and is a project thats monitors "the world's broadcast, print, and web news from nearly every corner of every country in over 100 languages and identifies the people, locations, organizations, themes, sources, emotions, counts, quotes, images and events driving our global society every second of every day, creating a free open platform for computing on the entire world." For this project, data were pulled from GDELT's Global Knowledge Graph Version 2 (GKG V2) database related the aforementioned candidates.  Specifically, the GDELT CKG values for tone, positive and negative scores, polarity and activity reference density and self reference density and a compilation of article themes were captured. 

Details of the process used to acquire, clean and store data can be found in the Poll_data_2016.ipynb and Google_BigQuery.ipynb notebooks available in the project GitHub repository.

 


#### Modeling data dictionary:


|Column        |Description    |
|-----------------|--------------------|
|end_time|  a date string correspondiong to a poll's end date|
|subject  | name of the subject of the press metrics|
|poll_result| the result for the subject in the poll ending on end_time|
|next_poll | a three-class classification variable for performance in the next poll (-1 = down, 0 = flat, 1 = up)|
|subject_end_time| a concatenation of subject and end date used for indexing|
|art_count  | the count of articles including the subject's name and within the time interval|
|word_count| the sum of the word counts of returned articles|
|tone_avg| the average of GDELT's tone measure for the returned articles|
|pos_score_avg  |the average of GDELT's positive score for the returned articles|
|neg_score_avg| the average of GDELT's negative score for the returned articles|
|polarity_avg| the average of GDELT's polarity measure for the returned articles|
|act_ref_den_avg  | the average of GDELT's active reference density measure for the returned articles|
|self_ref_den_avg|  the average of GDELT's self reference density measure for the returned articles|
|themes| a compilation of the themes for articles since the last poll (capped 2000)|

