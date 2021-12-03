import json
import os

spec_file = 'spec.json'
base_dir = '/home/azureuser/splits/'

batches = ['1kb', '10kb', '100kb', '1mb', '10mb', '100mb', '1gb', '1ms', '10ms', '100ms', '1s', '5s', '10s']
src_dirs = ['split_' + b + '_01_feb_ts' for b in batches]


def ingest(index, num=30):
    with open(spec_file) as ff:
        spec_json = json.load(ff)

    src_dir = src_dirs[index]
    size = batches[index]

    spec_json['spec']['ioConfig']['inputSource']['baseDir'] = base_dir + src_dir

    for i in range(num):
        spec_json['spec']['dataSchema']['dataSource'] = size + '_test_' + str(i)
        fil = open(spec_file, 'w')
        fil.write(json.dumps(spec_json))
        fil.close()
        os.system('~/apache-druid-0.22.0/bin/post-index-task --file spec.json --url http://localhost:8081')


for i in range(len(batches)):
    ingest(i)
