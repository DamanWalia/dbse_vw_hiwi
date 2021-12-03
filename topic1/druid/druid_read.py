import subprocess
import sys
from subprocess import check_output
sys.path.insert(1, '../parquet')

# from parquet.selectivities import selectivities
from selectivities import *

datasources = ["ss_01_feb", "ts_01_feb"]

for src in datasources:
    print("================================================================")
    print("Querying for ", src)

    print('Executing signal selectivities')
    for q in signal_selectivities:
        qstr = q[1].replace('tab1', src).replace('t <', '__time <')
        times = []

        for i in range(30):
            out = check_output(['/home/azureuser/apache-druid-0.22.0/bin/dsql', '-e', qstr]).decode('utf-8')
            times.append(float(out.strip().splitlines()[-1]))
        
        print('For sel:', q[0], ', average time:', (sum(times)/len(times)), 'ms')

    print('-------------------------------------')
    print('Executing time selectivities')
    for q in time_selectivities_2:
        qstr = q[1].replace('tab1', src).replace('t <', '__time <')
        times = []

        for i in range(30):
            out = check_output(['/home/azureuser/apache-druid-0.22.0/bin/dsql', '-e', qstr]).decode('utf-8')
            times.append(float(out.strip().splitlines()[-1]))
        
        print('For sel:', q[0], ', average time:', (sum(times)/len(times)), 'ms')
    