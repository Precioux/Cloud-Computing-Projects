import sys
import json

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

# Process each line from stdin
for line in sys.stdin:
    line = line.strip()
    candidate, state, src_num = line.split('\t')
    if state in States:
        if state == 'New York':
            tot_ny += 1
            if candidate == 'Both Candidates':
                biden_ny += 1
            if candidate == 'Donald Trump':
                trump_ny += 1
            if candidate == 'Joe Biden':
                both_ny += 1

        if state == 'Texas':
            tot_tx += 1
            if candidate == 'Both Candidates':
                biden_tx += 1
            if candidate == 'Donald Trump':
                trump_tx += 1
            if candidate == 'Joe Biden':
                both_tx += 1
        if state == 'California':
            tot_cl += 1
            if candidate == 'Both Candidates':
                biden_cl += 1
            if candidate == 'Donald Trump':
                trump_cl += 1
            if candidate == 'Joe Biden':
                both_cl += 1
        if state == 'Florida':
            tot_fl += 1
            if candidate == 'Both Candidates':
                biden_fl += 1
            if candidate == 'Donald Trump':
                trump_fl += 1
            if candidate == 'Joe Biden':
                both_fl += 1

biden = 'Joe Biden:'
trump = 'Donald Trump:'
both = 'Both Candidates:'
total = 'total:'
ny = 'New York:'
tx = 'Texas'
fl = 'Florida:'
cl = 'California:'

print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
        ny, biden,biden_ny/tot_ny,trump,trump_ny/tot_ny,both,both_ny/tot_ny,total,tot_ny))
print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
        cl, biden,biden_cl/tot_cl,trump,trump_cl/tot_cl,both,both_cl/tot_cl,total,tot_cl))
print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
        fl, biden,biden_fl/tot_fl,trump,trump_fl/tot_fl,both,both_fl/tot_fl,total,tot_fl))
print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
        tx, biden,biden_tx/tot_tx,trump,trump_tx/tot_tx,both,both_tx/tot_tx,total,tot_tx))