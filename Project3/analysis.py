import json
from mrjob.job import MRJob
import csv


class TweetAnalysis(MRJob):
    def mapper(self, _, line):
        global row_number
        # Use csv.reader to split the line correctly
        reader = csv.reader([line])
        columns = next(reader)

        if columns[0] == 'created_at':
            return
        tweet = columns[2]
        candidate = ''
        if ((
                    'Donald' or 'Trump' or 'donald' or 'trump' or 'DonaldTrump' or 'TRUMP' or 'realDonaldTrump' or '#Donald' or '#Trump' or '#donald' or '#trump' or '#DonaldTrump' or '#TRUMP' or '#realDonaldTrump') in tweet) and (
                (
                        'Joe' or 'joe' or 'Biden' or 'biden' or 'JoeBiden' or 'BIDEN' or '#Biden' or '#BidenHarris' or '#Joe' or '#joe' or '#Biden' or '#biden' or '#JoeBiden' or '#BIDEN') in tweet):
            candidate = 'Both Candidates'
        elif (
                'Donald' or 'Trump' or 'donald' or 'trump' or 'DonaldTrump' or 'TRUMP' or 'realDonaldTrump' or '#Donald' or '#Trump' or '#donald' or '#trump' or '#DonaldTrump' or '#TRUMP' or '#realDonaldTrump') in tweet:
            candidate = 'Donald Trump'
        elif (
                'Joe' or 'joe' or 'Biden' or 'biden' or 'JoeBiden' or 'BIDEN' or '#Biden' or '#BidenHarris' or '#Joe' or '#joe' or '#Biden' or '#biden' or '#JoeBiden' or '#BIDEN' or 'Obama' or '#Obama' or 'Harris' or '#Harris') in tweet:
            candidate = 'Joe Biden'
        else:
            candidate = 'Not recognized'

        data = {
            'candidate': candidate,
            'likes': float(columns[3]),
            'retweets': float(columns[4]),
            'source': columns[5]
        }

        yield None, json.dumps(data)

    def reducer(self, key, values):
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

        for value in values:
            data = json.loads(value)
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

        yield key, output1
        yield key, output2
        yield key, output3


if __name__ == '__main__':
    TweetAnalysis.run()
