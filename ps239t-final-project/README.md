Laura Jakli's Final Project 
PS239T

## Short Description

For this project, I use Facebook's Graph API and Twitter's API to collect and examine social media data, specifically pertaining to the 2016 U.S. Presidential Elections. Most of my data visualizations and
analyses are within the scope of traditional sentiment analysis, but Facebook's reactions feature allows
me to scrape and visualize reactions data as well. Although Facebook reactions are certainly not a direct match for sentiment analysis, these reactions provide some analytical leverage--especially in the post-election season as we grapple with how the public perceived each candidate, and how different strategic decisions, thematic appeals, and thematic campaign platforms contributed to the election results.

My Twitterscrape R code allowed me to track daily sentiment fluctuations toward each candidate on Twitter for the two weeks leading up to the election. Each day, I would collect the latest 4,000 tweets aimed at each candidate, and plot the sentiment outcome (-3 to 3) on a simple plot. The opinion lexicon I used to distinguish the sentiment of different words can be found at:

https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107/tree/master/data/opinion-lexicon-English



## Dependencies

The software my code depends on and version numbers:

1. R, version 3.1
2. Python 3.5.2, Anaconda 4.1.1 distribution.

## Files

This provides a list of all files contained in the repo, along with a brief description of each one:

### Data

1. DonaldTrump_facebook.csv: This dataset contains 16 columns scraped from Donald Trump's Official Facebook Page: a unique id for each status, the actual content of each message, the name of any links included in the status, the status type (photo, status, link), the actual individual link to the status, the time and date of its posting, and then a column for total reactions, as well as each individual reaction type (angry, wow, love, etc). 

2. hillaryclinton_facebook.csv: This dataset contains 16 columns scraped from Hillary Clinton's Official Facebook Page: a unique id for each status, the actual content of each message, the name of any links included in the status, the status type (photo, status, link), the actual individual link to the status, the time and date of its posting, and then a column for total reactions, as well as each individual reaction type (angry, wow, love, etc). 

3. govgaryjohnson_facebook.csv: This dataset contains 16 columns scraped from Gary Johnson's Official Facebook Page: a unique id for each status, the actual content of each message, the name of any links included in the status, the status type (photo, status, link), the actual individual link to the status, the time and date of its posting, and then a column for total reactions, as well as each individual reaction type (angry, wow, love, etc). 

4. drjillstein_facebook.csv: This dataset contains 16 columns scraped from Jill Stein's Official Facebook Page: a unique id for each status, the actual content of each message, the name of any links included in the status, the status type (photo, status, link), the actual individual link to the status, the time and date of its posting, and then a column for total reactions, as well as each individual reaction type (angry, wow, love, etc). 

### Code

1. 01_Twitterscrape.R: Collects data from the Twitter API and produces a plot of the sentiment toward each candidate (based on the latest 4,000 tweets directed at each candidate)

2. 02_Facebookscrapercode.py: Using the Facebook Graph API, this code scrapes the Facebook Pages of each of these candidates along the dimensions described in the data section and outputs each candidate's results in its own individual csv file.

3. 03_trumpstats.R: For Donald Trump, this code conducts descriptive analysis of the reactions data as well as different types of sentiment analyses, producing the tables and visualizations found in the Results directory.

4. 04_hillarystats.R: For Hillary Clinton, this code conducts descriptive analysis of the reactions data as well as different types of sentiment analyses, producing the tables and visualizations found in the Results directory.

5. 05_garyjohnsonstats.R: For Gary Johnson, this code conducts descriptive analysis of the reactions data as well as different types of sentiment analyses, producing the tables and visualizations found in the Results directory.

6. 06_jillsteinstats.R: For Jill Stein, this code conducts descriptive analysis of the reactions data as well as different types of sentiment analyses, producing the tables and visualizations found in the Results directory.


### Results

1. Daily_TwitterPart1.pdf: Organizes the plots produced by the first 4 days of the Twitter sentiment analysis.

2. Daily_TwitterPart2.pdf: Organizes the plots produced by the second 4 days of the Twitter sentiment analysis.

3. Daily_TwitterPart3.pdf: Organizes the plots produced by the third 4 days of the Twitter sentiment analysis.

4. Daily_TwitterPart4.pdf: Organizes the plots produced by the last 4 days of the Twitter sentiment analysis.

5. top_angrystatus_Trump.pdf: This is a table of the top 10 statuses (and date of status post) which received the most "angry" reactions.

6. top_angrystatus_Clinton.pdf: This is a table of the top 10 statuses (and date of status post) which received the most "angry" reactions.

7. top_angrystatus_Johnson.pdf: This is a table of the top 10 statuses (and date of status post) which received the most "angry" reactions.

8. top_angrystatus_Stein.pdf: This is a table of the top 10 statuses (and date of status post) which received the most "angry" reactions.

9. trumpanalysis.pdf: This is the knitted file from R, containing all commented code and data visualizations from the analysis pertaining to this candidate's Facebook Page.

10. clintonanalysis.pdf: This is the knitted file from R, containing all commented code and data visualizations from the analysis pertaining to this candidate's Facebook Page.

11. johnsonanalysis.pdf: This is the knitted file from R, containing all commented code and data visualizations from the analysis pertaining to this candidate's Facebook Page.

12. steinanalysis.pdf: This is the knitted file from R, containing all commented code and data visualizations from the analysis pertaining to this candidate's Facebook Page.

## More Information

I would like to give credit (as I did in my R and Python code) to the two most important sources for the "skeletons" of my Twitter and Facebook scrapers:

https://github.com/minimaxir/facebook-page-post-scraper

and 

##https://www.datascienceriot.com/how-to-use-r-to-scrape-tweets-super-tuesday-2016/kris/
