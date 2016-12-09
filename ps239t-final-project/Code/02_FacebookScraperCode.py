
# coding: utf-8

# In[73]:

#My task here is to scrape each presidential candidate's
#Facebook posts, and I use Facebook's Graph API to
#scrape data on the status, data, status type, and each reaction
#typology. This is done with the intention of performing a series
#of sentiment analyses in R, and also to get a better picture
#of the types of emotions(i.e., reactions) produced
#by different candidates, their language, and their social
#media presence. 

#The most helpful sample github code in producing a
#Facebook scraper came from 
#https://github.com/minimaxir. He has fantastic
#resources on how to scrape Facebook Pages.
#My biggest challenge was adapting the sample
#code to Python 3.


#First, let's import some important modules.
#CSV is for exporting the data in csv format. 
#The urllib. request module
#defines functions and classes which help in opening URLs.
#JSON encodes Python objects as JSON strings,
#and decode JSON strings into Python objects.
#Datetime supplies classes for manipulating dates/times.
#Time supplies similar functions 
#(used here for the sleep function).
#Codecs helps transcoding data. Using it here to
#work with Unicode text.


import urllib.request
import json
import datetime
import csv
import time
import codecs



# In[74]:

#Need to sign up for a Facebook developer account for these.
#I'm commenting this out for privacy purposes.

app_id = "XXXXXXXXXXXXXX"
app_secret = "XXXXXXXXXXXXXXXX" 

#Here, can go through each page id at a time, to 
#produce 4 csv files in total.

#page_id = "DonaldTrump"
#page_id = "hillaryclinton"
#page_id = "govgaryjohnson"
#page_id = "drjillstein"

#Finally, the access token can be generated with the app_id and app_secret.

access_token = app_id + "|" + app_secret


# In[1]:

#Here, we define a function that helps us do repeated
#requests until one succeeds. The urllib module 
#allows us to access a certain website. 
#The time.sleep function is important in that 
#to make a Python program delay (pause execution), 
#we can use the time.sleep method. We use this to
#prevent making too many requests in a short time 
#span.

def request_until_succeed(url):
    req = urllib.request.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib.request.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)

            print("Error for URL %s: %s" % (url, datetime.datetime.now()))
            print("Retrying.")

    return response.read().decode(response.headers.get_content_charset())


# This function provides unicode support for writing to csv.
# Reference this blog for the future on this if stuck:
# http://johntilelli.com/blog/update/2016/06/20/analysis
#-of-pres-coverage-facebook-cnn-page.html

def unicode_normalize(text):
    return text.translate({ 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22,
                            0xa0:0x20 })

#Function to help create the URL string and set
#reactions parameters for all of the Facebook Page data 
def getFacebookPageFeedData(page_id, access_token, num_statuses):

    base = "https://graph.facebook.com/v2.6"
    node = "/%s/posts" % page_id 
    fields = "/?fields=message,link,created_time,type,name,id," +             "comments.limit(0).summary(true),shares,reactions" +             ".limit(0).summary(true)"
    parameters = "&limit=%s&access_token=%s" % (num_statuses, access_token)
    url = base + node + fields + parameters

    # retrieve data
    data = json.loads(request_until_succeed(url))

    return data

#Function for creating all of the reactions parameters.
#Here's a helpful stackoverflow page on this:
#http://stackoverflow.com/questions/36930414/how-can-
#i-get-facebook-graph-api-reaction-summary-count-separately
#/37239851#37239851

def getReactionsForStatus(status_id, access_token):


    base = "https://graph.facebook.com/v2.6"
    node = "/%s" % status_id
    reactions = "/?fields="             "reactions.type(LIKE).limit(0).summary(total_count).as(like)"             ",reactions.type(LOVE).limit(0).summary(total_count).as(love)"             ",reactions.type(WOW).limit(0).summary(total_count).as(wow)"             ",reactions.type(HAHA).limit(0).summary(total_count).as(haha)"             ",reactions.type(SAD).limit(0).summary(total_count).as(sad)"             ",reactions.type(ANGRY).limit(0).summary(total_count).as(angry)"
    parameters = "&access_token=%s" % access_token
    url = base + node + reactions + parameters

    data = json.loads(request_until_succeed(url))

    return data


#Since the Facebook status is now set
#up as Python dictionary, 
#we call the key.

def processFacebookPageFeedStatus(status, access_token):

# As you see in the if else statements, 
# When items don't exist,
# check for existence first.

    status_id = status['id']
    status_message = '' if 'message' not in status.keys() else             unicode_normalize(status['message'])
    link_name = '' if 'name' not in status.keys() else             unicode_normalize(status['name'])
    status_type = status['type']
    status_link = '' if 'link' not in status.keys() else             unicode_normalize(status['link'])

#Because the time is in a crazy format, reference 
#following stackoverflow page in how to get it 
#into workable csv format.
#http://stackoverflow.com/questions/34331136/scrape-facebook-attributeerror

    status_published = datetime.datetime.strptime(
            status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published +             datetime.timedelta(hours=-5) 
    status_published = status_published.strftime(
            '%Y-%m-%d %H:%M:%S') 

# Here, we're chaining dictionary lookups (since they're nested)

    num_reactions = 0 if 'reactions' not in status else             status['reactions']['summary']['total_count']
    num_comments = 0 if 'comments' not in status else             status['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in status else status['shares']['count']

#Although we have collected data for the entire history of each
#Facebook page, reactions weren't around until February 24th of this year.
#As such, we have to specify gathering data on Facebook reactions
#after this feature was rolled out. 

    reactions = getReactionsForStatus(status_id, access_token) if             status_published > '2016-02-24 00:00:00' else {}

    num_likes = 0 if 'like' not in reactions else             reactions['like']['summary']['total_count']

#We also have to now set the number of Facebook Likes equal to
#Number of reactions for statuses before that Febryary 24th rollout
#date.

    num_likes = num_reactions if status_published < '2016-02-24 00:00:00'             else num_likes

    def get_num_total_reactions(reaction_type, reactions):
        if reaction_type not in reactions:
            return 0
        else:
            return reactions[reaction_type]['summary']['total_count']

    num_loves = get_num_total_reactions('love', reactions)
    num_wows = get_num_total_reactions('wow', reactions)
    num_hahas = get_num_total_reactions('haha', reactions)
    num_sads = get_num_total_reactions('sad', reactions)
    num_angrys = get_num_total_reactions('angry', reactions)

#Now, we return a 15-tuple (tuples are like lists, but immutable)

    return (status_id, status_message, link_name, status_type, status_link,
            status_published, num_reactions, num_comments, num_shares,
            num_likes, num_loves, num_wows, num_hahas, num_sads, num_angrys)

#Now we write all of this to a csv file, keeping count of 
#how many have been processed. We make sure it's utf-8 encoded.

def scrapeFacebookPageFeedStatus(page_id, access_token):
    with open('%s_facebook_statuses.csv' % page_id, 'w', newline='',encoding='utf-8') as file:
        w = csv.writer(file)
        w.writerow(["status_id", "status_message", "link_name", "status_type",
                    "status_link", "status_published", "num_reactions", 
                    "num_comments", "num_shares", "num_likes", "num_loves", 
                    "num_wows", "num_hahas", "num_sads", "num_angrys"])

        has_next_page = True
        num_processed = 0   
        scrape_starttime = datetime.datetime.now()

        print("Scraping %s Facebook Page: %s\n" % (page_id, scrape_starttime))

        statuses = getFacebookPageFeedData(page_id, access_token, 100)

        while has_next_page:
            for status in statuses['data']:

                # Check to see if status has the expected data parameters
                if 'reactions' in status:
                    w.writerow(processFacebookPageFeedStatus(status,
                        access_token))

                #We do periodical output to check that everything is
                #working correctly.
                num_processed += 1
                if num_processed % 100 == 0:
                    print("%s Statuses Processed: %s" %                         (num_processed, datetime.datetime.now()))

            #Once there is no more "next page" we're done. We use
            #a simple if else statement for this.
            if 'paging' in statuses.keys():
                statuses = json.loads(request_until_succeed(
                                        statuses['paging']['next']))
            else:
                has_next_page = False

        #Finally, print and return all of this.
        print("\nDone!\n%s Statuses Processed in %s" %             (num_processed, datetime.datetime.now() - scrape_starttime))


if __name__ == '__main__':
    scrapeFacebookPageFeedStatus(page_id, access_token)

