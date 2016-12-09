####TWITTER DATA BEFORE THE ELECTION####

##My task here was just to estimate the daily changes and overall trends
##in Twitter sentiment towards each presidential candidate in comparison
##to the other candidates. I built a tweet scraper, and thankfully,
##these scrapers are relatively simple to build because
##they are so well documented online. The best source for me was
##the following website/sample code:
##https://www.datascienceriot.com/how-to-use-r-to-scrape-tweets-super-tuesday-2016/kris/
##I wanted to examine whether big events 
##(such as the Comey investigation) would impact sentiment on this
##social media platform. Although I find some evidence for certain
##events having some effect, there is also a large amount of
##normal fluctuation in sentiment toward each candidate on a
##daily basis. Generally, Gov. Gary Johnson had the consistently
##"least" negative sentiment directed toward him on this social media
##platform. 

#First, let's set working directory
setwd("/Users/laurajakli/Desktop/231A_data")

#Don't need as many packages here
library(twitteR)
library(ROAuth)
library(httr)
library(plyr)
library(stringr)
library(ggplot2)

#Here I set my API Keys, which I will now comment out

#api_key <- "SECRET"
#api_secret <- "SECRET"
#access_token <- "SECRET"
#access_token_secret <- "SECRET"
#setup_twitter_oauth(api_key, api_secret, access_token, access_token_secret)

#I did this for about the last 2 weeks of the election, once a day.
#Pulling the latest 4000 tweets aimed at each candidate using 
#the searthTwitter function.
tweets_trump <- searchTwitter('@realDonaldTrump', n=4000)
tweets_clinton <- searchTwitter('@HillaryClinton', n=4000)
tweets_stein<- searchTwitter('@DrJillStein', n=4000)
tweets_johnson <- searchTwitter('@GovGaryJohnson', n=4000)


#This is used to get the text from each tweet
feed_clinton = laply(tweets_clinton, function(t) t$getText())
feed_trump = laply(tweets_trump, function(t) t$getText())
feed_stein = laply(tweets_stein, function(t) t$getText())
feed_johnson = laply(tweets_johnson, function(t) t$getText())


#Now, we still have to read in a dictionary
#of positive and negative words for the sentiment analysis.
#I added some recommended words and made "nasty" a positive
#term because most people were using it sarcastically
#during this period.

yay = scan('opinion-lexicon-English/positive-words.txt',
           what='character', comment.char=';')
boo = scan('opinion-lexicon-English/negative-words.txt',
           what='character', comment.char=';')
# Add a few twitter-specific negative phrases
bad_text = c(boo, 'wtf', 'epicfail', 'douchebag')
good_text = c(yay, 'upgrade', ':)', '#iVoted', 'voted', 'nasty')

#Here is the actual brute work behind the sentiment scoring.
#Since we want this function to return a scoring array, 
#we use the laply function from plyr.
score.sentiment = function(sentences, good_text, bad_text, .progress='none')
{
  scores = laply(sentences, function(sentence, good_text, bad_text) {
    
    # We can also use the R regex-driven global substitute to clean up our code
    # (i.e., remove emojis, split words, make sure everything is in unicode format, 
    #change letters to lowercase, etc.
    #Similar to the set up we had with the Facebook status
    #sentiment analysis and wordcloud prep. 
    #This github link was super helpful here, and also
    #has the code for unlisting the list, which is not
    #intuitive but may be helpful in the future:
    #https://github.com/jeffreybreen/twitter-sentiment
    #-analysis-tutorial-201107/blob/master/R/sentiment.R
    sentence = gsub('[[:punct:]]', '', sentence)
    sentence = gsub('[[:cntrl:]]', '', sentence)
    sentence = gsub('\\d+', '', sentence)
    sentence <- iconv(sentence, 'UTF-8', 'ASCII')
    sentence = tolower(sentence)        
    word.list = str_split(sentence, '\\s+')
    words = unlist(word.list)
    
    #With this match function, we're actually doing the work of
    #comparing the words in the scraped tweets to the positive/
    #negative sentiments in the dictionary.
    #It then returns the position of the match or produces
    # an NA. 
    pos.matches = match(words, good_text)
    neg.matches = match(words, bad_text)
    pos.matches = !is.na(pos.matches)
    neg.matches = !is.na(neg.matches)
    
    #Here, the matches are treated as a 1/0 by 
    #the sum function.
    score = sum(pos.matches) - sum(neg.matches)
    
    #Finally, we return the scores in a dataframe.
    return(score)
  }, good_text, bad_text, .progress=.progress )
  
  scores.df = data.frame(score=scores, text=sentences)
  return(scores.df)
}


# Now, the scores are retreived  and we also link to the candidate name.
thedonald <- score.sentiment(feed_trump, good_text, bad_text, .progress='text')
thedonald$name <- 'Trump'
clinton <- score.sentiment(feed_clinton, good_text, bad_text, .progress='text')
clinton$name <- 'Clinton'
stein <- score.sentiment(feed_stein, good_text, bad_text, .progress='text')
stein$name <- 'Stein'
johnson <- score.sentiment(feed_johnson, good_text, bad_text, .progress='text')
johnson$name <- 'Johnson'

# We merge this into one aggregated dataframe.
# We clean this in a few ways before we plot.
# First, we remove the text, because we care
# about the sentiment here. We also remove really
# extreme outlier scores in both directions, as well
# as completely neutral ones (0's). I am losing
# some good information by making this choice, but
# the neutral words would essentially drown out
# the rest of the terms in the plot and make it 
# look crazy, and this is also
# a common practice among others who do twitter sentiment
# analysis.

plotdat <- rbind(thedonald, clinton, stein, johnson)
plotdat <- plotdat[c("name", "score")]
plotdat <- plotdat[!plotdat$score == 0, ]
plotdat <- plotdat[!plotdat$score > 3, ]
plotdat <- plotdat[!plotdat$score < (-3), ]

#Finally, I do a basic plot. All of my plots are
#going to be uploaded for each day, and each
#plot's file name will indicate the date
#to which it pertains.

qplot(factor(score), data=plotdat, geom="bar", 
      fill=factor(name),
      xlab = "Sentiment Score")


