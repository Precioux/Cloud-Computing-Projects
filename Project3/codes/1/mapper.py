import sys
import csv
import json

def process_tweets():
    # Read the input from stdin
    lines = sys.stdin.readlines()

    # Determine the delimiter used in the CSV file
    dialect = csv.Sniffer().sniff(lines[0])
    delimiter = dialect.delimiter

    # Process each line as a CSV record
    csv_reader = csv.reader(lines, delimiter=delimiter)
    for columns in csv_reader:
        if columns[0] == 'created_at':
            continue

        tweet = columns[2]
        candidate = ''
        if (
            ('Donald' or 'Trump' or 'donald' or 'trump' or 'DonaldTrump' or 'TRUMP' or 'realDonaldTrump' or '#Donald' or '#Trump' or '#donald' or '#trump' or '#DonaldTrump' or '#TRUMP' or '#realDonaldTrump') in tweet
            and ('Joe' or 'joe' or 'Biden' or 'biden' or 'JoeBiden' or 'BIDEN' or '#Biden' or '#BidenHarris' or '#Joe' or '#joe' or '#Biden' or '#biden' or '#JoeBiden' or '#BIDEN') in tweet
        ):
            candidate = 'Both Candidates'
        elif (
            ('Donald' or 'Trump' or 'donald' or 'trump' or 'DonaldTrump' or 'TRUMP' or 'realDonaldTrump' or '#Donald' or '#Trump' or '#donald' or '#trump' or '#DonaldTrump' or '#TRUMP' or '#realDonaldTrump') in tweet
        ):
            candidate = 'Donald Trump'
        elif (
            ('Joe' or 'joe' or 'Biden' or 'biden' or 'JoeBiden' or 'BIDEN' or '#Biden' or '#BidenHarris' or '#Joe' or '#joe' or '#Biden' or '#biden' or '#JoeBiden' or '#BIDEN' or 'Obama' or '#Obama' or 'Harris' or '#Harris') in tweet
        ):
            candidate = 'Joe Biden'
        else:
            candidate = 'Not recognized'

        data = {
            'candidate': candidate,
            'likes': float(columns[3]),
            'retweets': float(columns[4]),
            'source': columns[5]
        }

        print(json.dumps(data))

# Call the function to process the tweets
process_tweets()
