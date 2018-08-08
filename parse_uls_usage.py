#!/usr/bin/env/python
"""
Timer
2932 = 11 seconds
157046 = 2:37 seconds = 157 seconds
0 = 0 seconds
"""

import ConfigParser
import glob
import io
import os
import pickle


ddir = "C:\\ProgramData\\ULSMVX"
#ddir = "."
raw_out_filename = 'uls_usage_raw.p'
csv_out_filename = 'uls_usage.csv'

# get files
fns = glob.glob(
    os.path.join(os.path.expanduser(ddir), '*.DAT'))

fn_to_index = lambda fn: int(
    os.path.splitext(os.path.basename(fn))[0].split('ULS')[1])
fns.sort(key=fn_to_index)

jobs = []
for fn in fns:
    p = ConfigParser.ConfigParser()
    with io.open(fn, 'r', encoding='utf-16') as fp:
        p.readfp(fp)
    info = dict(p.items('PRINTJOB'))
    info['filename'] = fn
    info['index'] = fn_to_index(fn)
    info['ctime'] = os.path.getctime(info['printfile'])  # unix timestamp
    jobs.append(info)

with open(raw_out_filename, 'w') as f:
    pickle.dump(jobs, f)

# make csv
# index, job name, time, duration
with open(csv_out_filename, 'w') as f:
    f.write("#index, job name, time, duration\n")
    for j in jobs:
        f.write("%i, '%s', %f, %s\n" % (
            j['index'], j['jobname'].replace(',', '_'),
            j['ctime'], float(j['timer']) / 1000.,))