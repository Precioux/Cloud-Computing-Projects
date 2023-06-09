import sys
import json

def process_tweets():
    # Initialize variables
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
        data = json.loads(line)
        candidate = data['candidate']
        likes = data['likes']
        retweets = data['retweets']
        source = data['source']

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

    # Output the results
    output1 = f"Joe Biden    likes: {biden_likes}    retweets: {biden_rets}      Twitter Web App: {biden_web}    Twitter for iPhone: {biden_iphone}      Twitter for Android: {biden_android}"
    output2 = f"Donald Trump    likes: {trump_likes}    retweets: {trump_rets}      Twitter Web App: {trump_web}    Twitter for iPhone: {trump_iphone}      Twitter for Android: {trump_android}"
    output3 = f"Both Candidates     likes: {both_likes}     retweets: {both_rets}       Twitter Web App: {both_web}     Twitter for iPhone: {both_iphone}       Twitter for Android: {both_android}"

    print(output1)
    print(output2)
    print(output3)

# Call the function to process the tweets
process_tweets()
