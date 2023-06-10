import json
from mrjob.job import MRJob
import csv
from datetime import datetime
biden_ny = 0
biden_tx = 0
biden_cl = 0
biden_fl = 0
tot_ny=0
tot_tx=0
tot_cl=0
tot_fl=0
trump_ny = 0
trump_tx = 0
trump_cl = 0
trump_fl = 0
both_ny = 0
both_tx = 0
both_cl = 0
both_fl = 0
States = {'New York', 'Texas', 'California', 'Florida'}

class TweetAnalysis(MRJob):
    def mapper(self, _, line):
        global row_number
        # Use csv.reader to split the line correctly
        reader = csv.reader([line])
        columns = next(reader)
        if columns[0] == 'created_at':
            return
        date_string = columns[0]
        date_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        hour = date_object.hour
        state = columns[18]
        candidate = ''

        if state in States:
            if 9 <= hour <= 17:
                tweet = columns[2]
                if ('Donald' or 'Trump' or 'donald' or 'trump' or 'DonaldTrump' or 'TRUMP' or 'realDonaldTrump' or '#Donald' or '#Trump' or '#donald' or '#trump' or '#DonaldTrump' or '#TRUMP' or '#realDonaldTrump') in tweet and ('Joe' or 'joe' or 'Biden' or 'biden' or 'JoeBiden' or 'BIDEN' or '#Biden' or '#BidenHarris' or '#Joe' or '#joe' or '#Biden' or '#biden' or '#JoeBiden' or '#BIDEN') in tweet:
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
            'state': state,
            'hour' : hour
        }

        yield None, json.dumps(data)

    def reducer(self, key, values):
        global tot_ny, both_ny, trump_ny, tot_tx, both_tx, trump_tx, tot_cl, both_cl, trump_cl, both_fl, tot_fl, trump_fl, biden_fl, biden_tx, biden_ny, biden_cl
        output = ''
        for value in values:
            data = json.loads(value)
            candidate = data['candidate']
            state = data['state']
            if state in States:
                if state == 'New York':
                    tot_ny+=1
                    if candidate == 'Both Candidates':
                        biden_ny+=1
                    elif candidate == 'Donald Trump':
                        trump_ny+=1
                    elif candidate == 'Joe Biden':
                        both_ny=+1
                if state == 'Texas':
                    tot_tx+=1
                    if candidate == 'Both Candidates':
                        biden_tx+=1
                    elif candidate == 'Donald Trump':
                        trump_tx+=1
                    elif candidate == 'Joe Biden':
                        both_tx=+1
                if state == 'California':
                    tot_cl+=1
                    if candidate == 'Both Candidates':
                        biden_cl+=1
                    elif candidate == 'Donald Trump':
                        trump_cl+=1
                    elif candidate == 'Joe Biden':
                        both_cl=+1
                if state == 'Florida':
                    tot_fl+=1
                    if candidate == 'Both Candidates':
                        biden_fl+=1
                    elif candidate == 'Donald Trump':
                        trump_fl+=1
                    elif candidate == 'Joe Biden':
                        both_fl=+1



        output1 =f'california {biden_cl} {trump_cl} {both_cl} {tot_cl}'
        output2 = f'newyork {biden_ny} {trump_ny} {both_ny} {tot_ny}'
        output3 = f'texas  {biden_tx} {trump_tx} {both_tx} {tot_tx}'
        output4 = f'florida {biden_fl} {trump_fl} {both_fl} {tot_fl}'

        yield key, output1
        yield key, output2
        yield key, output3
        yield key, output4


if __name__ == '__main__':
    TweetAnalysis.run()
