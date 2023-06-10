#!/usr/bin/env python3
import sys
import csv
import json

for line in sys.stdin:

    reader = csv.reader([line])
    columns = next(reader)

    if line.startswith("created_at"):
        continue

    tweet = columns[2]
    candidate = ''
    if ('Donald' or 'Trump' or 'donald' or 'trump' or 'DonaldTrump' or 'TRUMP' or 'realDonaldTrump' or '#Donald' or '#Trump' or '#donald' or '#trump' or '#DonaldTrump' or '#TRUMP' or '#realDonaldTrump') in tweet and ('Joe' or 'joe' or 'Biden' or 'biden' or 'JoeBiden' or 'BIDEN' or '#Biden' or '#BidenHarris' or '#Joe' or '#joe' or '#Biden' or '#biden' or '#JoeBiden' or '#BIDEN') in tweet:
            candidate = 'Both Candidates'
    elif ('Donald' or 'Trump' or 'donald' or 'trump' or 'DonaldTrump' or 'TRUMP' or 'realDonaldTrump' or '#Donald' or '#Trump' or '#donald' or '#trump' or '#DonaldTrump' or '#TRUMP' or '#realDonaldTrump') in tweet:
            candidate = 'Donald Trump'
    elif ('Joe' or 'joe' or 'Biden' or 'biden' or 'JoeBiden' or 'BIDEN' or '#Biden' or '#BidenHarris' or '#Joe' or '#joe' or '#Biden' or '#biden' or '#JoeBiden' or '#BIDEN' or 'Obama' or '#Obama' or 'Harris' or '#Harris') in tweet:
            candidate = 'Joe Biden'
    else:
            candidate = 'Not recognized'
    likes = float(columns[3])
    retweets = float(columns[4])
    source = columns[5]
    print('%s\t%s\t%s\t%s\t%s' % (candidate, likes, retweets, source, 1))

