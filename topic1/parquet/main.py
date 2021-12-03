import os
import argparse

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

from selectivities import *

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='Path of the directory where json files are located')
args = parser.parse_args()

conf = SparkConf()
conf.set('spark.driver.memory', '16g')
conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
sparkCtx = SparkContext(conf=conf)

spark = SparkSession(sparkContext=sparkCtx) \
    .builder \
    .appName("Parquet test") \
    .getOrCreate()

out_dir = 'out'
if not os.path.exists(out_dir):
    os.mkdir(out_dir)


def get_file_extension(file_path):
    return os.path.splitext(os.path.basename(file_path))[1]


def write_to_parquet(dir_path):
    for fil in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, fil)) and get_file_extension(fil) == '.json':
            print('Reading ', fil)
            tab = spark.read.json(os.path.join(dir_path, fil))
            print('Writing as parquet')
            tab.write.mode('overwrite').parquet(os.path.join(out_dir, fil + '.parquet'))


def read_from_parquet(table, query_index, signal_wise=True):
    import time
    sel = signal_selectivities[query_index][0] if signal_wise else time_selectivities[query_index][0]
    t1 = time.time()
    for i in range(30):
        if signal_wise:
            spark.sql(signal_selectivities[query_index][1])
        else:
            spark.sql(time_selectivities[query_index][1])
    print("==========================================================================")
    print('Sel:', sel, "time:", (time.time() - t1) * 1000 / 30, "ms")
    print("==========================================================================")


import time

# write_to_parquet(args.i)
# times = []
# for i in range(30):
#     t1 = time.time()
#     write_to_parquet(args.i, i)
#     times.append(time.time() - t1)

# print('Average time to write', args.i, 'is', sum(times) / len(times), 'ms')


ddirs = ["out/01_feb_ss.json.parquet", "out/01_feb_ts.json.parquet"]
ddir = ddirs[1]
print('Reading file:', ddir)
tab = spark.read.parquet(ddir)
tab.createOrReplaceTempView('tab1')

which = args.i[0]
ind = int(args.i[1:])

if which == 's' and ind < len(signal_selectivities):
    read_from_parquet(tab, ind, True)
elif ind < len(time_selectivities):
    read_from_parquet(tab, ind, False)
else:
    print('Done')


# print('Signal selectivities')
# for i in range(len(signal_selectivities)):
#     read_from_parquet(tab, i, True)

# print('Time selectivities')
# for i in range(len(time_selectivities)):
#     read_from_parquet(tab, i, False)
