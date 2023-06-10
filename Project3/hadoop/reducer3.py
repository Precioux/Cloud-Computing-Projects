import sys
import json

biden_ny = 0
biden_cl = 0
tot_ny=0
tot_cl=0
trump_ny = 0
trump_cl = 0
both_ny = 0
both_cl = 0
States = {'New York', 'California'}

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

        if state == 'California':
            tot_cl += 1
            if candidate == 'Both Candidates':
                biden_cl += 1
            if candidate == 'Donald Trump':
                trump_cl += 1
            if candidate == 'Joe Biden':
                both_cl += 1

biden = 'Joe Biden:'
trump = 'Donald Trump:'
both = 'Both Candidates:'
total = 'total:'
ny = 'New York:'
cl = 'California:'

print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
        ny, biden,biden_ny/tot_ny,trump,trump_ny/tot_ny,both,both_ny/tot_ny,total,tot_ny))
print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
        cl, biden,biden_cl/tot_cl,trump,trump_cl/tot_cl,both,both_cl/tot_cl,total,tot_cl))
