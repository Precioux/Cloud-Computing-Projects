#!/usr/bin/env python3
import sys
import csv
import json
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

for line in sys.stdin:

    reader = csv.reader([line])
    columns = next(reader)

    if line.startswith("created_at"):
        continue

    date_string = columns[0]
    date_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    hour = date_object.hour
    state = columns[18]
    candidate = 'none'

    if state in States:
        if 9 <= hour <= 17:
            tweet = columns[2]
            if (
                    'Donald' or 'Trump' or 'donald' or 'trump' or 'DonaldTrump' or 'TRUMP' or 'realDonaldTrump' or '#Donald' or '#Trump' or '#donald' or '#trump' or '#DonaldTrump' or '#TRUMP' or '#realDonaldTrump') in tweet and (
                    'Joe' or 'joe' or 'Biden' or 'biden' or 'JoeBiden' or 'BIDEN' or '#Biden' or '#BidenHarris' or '#Joe' or '#joe' or '#Biden' or '#biden' or '#JoeBiden' or '#BIDEN') in tweet:
                candidate = 'Both Candidates'
            elif (
                    'Donald' or 'Trump' or 'donald' or 'trump' or 'DonaldTrump' or 'TRUMP' or 'realDonaldTrump' or '#Donald' or '#Trump' or '#donald' or '#trump' or '#DonaldTrump' or '#TRUMP' or '#realDonaldTrump') in tweet:
                candidate = 'Donald Trump'
            elif (
                    'Joe' or 'joe' or 'Biden' or 'biden' or 'JoeBiden' or 'BIDEN' or '#Biden' or '#BidenHarris' or '#Joe' or '#joe' or '#Biden' or '#biden' or '#JoeBiden' or '#BIDEN' or 'Obama' or '#Obama' or 'Harris' or '#Harris') in tweet:
                candidate = 'Joe Biden'
            else:
                candidate = 'Not recognized'

    print('%s\t%s\t%s' % (candidate, state, 1))

