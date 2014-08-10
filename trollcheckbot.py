
"""
Trollcheckbot, Copyright 2014 Whenido, /u/tingmakpuk. Open source license available.
Reddit bot to be summoned by a user responding to an exising comment using
a trigger phrase.  The bot will report on the user who posted the parent comment:

Version 1.0: Replies with target username and comment karma.
Version 1.1: Replies with target username and comment karma.  Makes a judgement.
Version 1.1a: Fixed signature and related bug
Version 1.1b: Incorporating some of the recommendations by /u/gengisteve - Thanks 'gs'
WIP -- Version 1.2 will correct the bug related to self check.
WIP -- Version 2.0 will log and avoid duplication
WIP -- Version 2.1 will log trolls, and offer a special note if trolls are labeled 'mostly harmless'

"""


#known bugs:
#If trollcheckbot checks itself, it will pick up on its own reported username as a trigger
    #on the next cycle. 
#Not currently logging work, so duplicates effort, and reddit not blocking dupl commments anymore?


#config:

import praw
import time #need for .sleep
import datetime #to be used later to log


user_agent = ("Troll Check Bot 1.1a by /u/tingmakpuk"  
            "https://github.com/tingmakpuk/")

r = praw.Reddit(user_agent=user_agent)
me = 'trollcheckbot'
r.login(me, '') #remove password before posting!
runtime = 0
successtime = 0

checkWords = set(["trollcheckbot", "trollcheck"]) #Setting up for checkit #per gs: sets work faster than lists
subreddit = r.get_subreddit('whenido')  #test with 1 sub; 'all' for full deployment?
signature = ("\n\n"  #gs rec for shorter lines
        "[Sourcecode](https://github.com/tingmakpuk/) | "
        "[Mods may unsubscribe here.]"
        "(http://www.reddit.com/message/compose/?to=tingmakpuk&subject=bot&message=%2Bunsub%20/r/%28subname%29)")

"""
Saving/crediting resources:
Reddit 1 - http://praw.readthedocs.org/en/latest/pages
    /getting_started.html#breaking-down-redditor-karma-by-subreddit
Reddit 2 - https://github.com/reddit/reddit/wiki/API

Inspire 1 https://github.com/Damgaard/Reddit-Bots/blob/master/karma_breakdown.py
Inspire 2 https://github.com/kaare8p/Dogecoin-tipper/blob/master/Dogecoin-tipper.py
"""


def get_comments(subreddit): #gs rec for pulling out functions like...

    try:
        print "Checking comments." #debug checkpoint
        comments = subreddit.get_comments(limit = 100)
        return comments
    
    except: #not sure what error I would see here, but...
        print "Failed to get comments." #adding for debug checkpoint.

while True:  #checking for summons
    for post in get_comments(subreddit):
        summon_author = post.author  #use later to create a more personalized response?
        summon_text = post.body.lower()

        checkit = any(string in summon_text for string in checkWords)

        if checkit:  #if summoned, report
            print "Found one." #debug checkpoint
                
            parent_author = r.get_info(thing_id=post.parent_id).author
            str_parent = str(parent_author)
            print str_parent #debug checkpoint
                
            get_karma = parent_author.comment_karma
            str_karma = str(get_karma)
            print str_karma #debug checkpoint
                
            if get_karma > 200:
                judgement = "Not a professional troll."
            elif get_karma  >= 0:
                judgement = "You make the call."
            else:
                judgement = "Don't feed the troll."
            """    
            #Is this a new python 3 format or something?  Program keeps crashing here.  Reverting.
            comment_reply = ('/u/{} has {} comment karma.  {}'.format( #per gs: new format option 
                str_parent,
                str_karma,
                judgement)
            """
            comment_reply = ("/u/" + str_parent + " has " + str_karma + " comment karma.  " + judgement)    
            print comment_reply #+ signature #debug checkpoint

            try:
                post.reply(comment_reply + signature) #pull for debug
                successtime += 1
                
            except: #someerror: #gs recs catching spec errors, but how?
                runtime += 1
                if runtime == 100:
                    print
                    print "Success/Run: " + str(successtime) + "/" + str(runtime)
                    break
                time.sleep(25)
                print "Slept 25." #debug checkpoint
                continue
     
            time.sleep(15)
            print "Slept 15." #debug checkpoint
        
            runtime += 1
            if runtime == 100:
                print
                print "Success/Run: " + str(successtime) + "/" + str(runtime)
                break

        
