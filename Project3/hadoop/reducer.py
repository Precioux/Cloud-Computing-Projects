import sys
import json

biden_likes = 0
biden_iphone = 0
biden_android = 0
biden_web = 0
biden_rets = 0
trump_likes = 0
trump_iphone = 0
trump_android = 0
trump_web = 0
trump_rets = 0
both_likes = 0
both_iphone = 0
both_android = 0
both_web = 0
both_rets = 0

# Process each line from stdin
for line in sys.stdin:
    line = line.strip()
    candidate, likes_input, retweets_input, source, src_num = line.split('\t')
    likes = float(likes_input)
    retweets = float(retweets_input)
    if candidate == 'Joe Biden':
        biden_likes += likes
        biden_rets += retweets
        if source == 'Twitter for iPhone':
            biden_iphone += 1
        elif source == 'Twitter for Android':
            biden_android += 1
        elif source == 'Twitter Web App':
            biden_web += 1

    elif candidate == 'Donald Trump':
        trump_likes += likes
        trump_rets += retweets
        if source == 'Twitter for iPhone':
            trump_iphone += 1
        elif source == 'Twitter for Android':
            trump_android += 1
        elif source == 'Twitter Web App':
            trump_web += 1

    elif candidate == 'Both Candidates':
        both_likes += likes
        both_rets += retweets
        if source == 'Twitter for iPhone':
            both_iphone += 1
        elif source == 'Twitter for Android':
            both_android += 1
        elif source == 'Twitter Web App':
            both_web += 1

biden = 'Joe Biden'
trump = 'Donald Trump'
both = 'Both Candidates'
likes_str = 'likes:'
retweets_str = 'retweets:'
web = 'Twitter Web App:'
ios = 'Twitter for iPhone:'
android = 'Twitter for Android:'

print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
    biden, likes_str, biden_likes, retweets_str, biden_rets, web, biden_web, ios, biden_iphone, android, biden_android))
print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
    trump, likes_str, trump_likes, retweets_str, trump_rets, web, trump_web, ios, trump_iphone, android, trump_android))
print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
    both, likes_str, both_likes, retweets_str, both_rets, web, both_web, ios, both_iphone, android, both_android))
