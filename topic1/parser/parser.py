import argparse
import faulthandler
import json
import os
import shutil
import time

import ijson

# Handle commandline arguments

parser = argparse.ArgumentParser(description='Converts the VW time data into a format suitable for time series '
                                             'database ingestion')
parser.add_argument('-i', help='The path of the input file')
parser.add_argument('-n', help='The number of entries', type=int, default=10 ** 6)
parser.add_argument('-f', help='The output format of the data. [json, csv]', default='json')
parser.add_argument('-o', help='The ordering of the output. [none, t, s]', default='none')
args = parser.parse_args()

out_dir = "out"
metadata_dir = "out/metadata"


def check_args():
    if args.f not in ['json', 'csv']:
        raise ValueError('Format must be either json or csv')


def write_header(file):
    file.write(",".join(['t', 's', 'tid', 'sid']) + '\n')


def write_metadata_header(file):
    file.write(",".join(['tid', 'sid', 'time_factor', 'time_offset', 'signal_factor', 'signal_offset', 'unit']) + '\n')


def create_subdir(out, file_path):
    subdir_path = os.path.join(out_dir, os.path.splitext(os.path.basename(file_path))[0])
    if os.path.isdir(subdir_path):
        shutil.rmtree(subdir_path)
    os.mkdir(subdir_path)
    return subdir_path


def create_outfile(subdir_path, part_number):
    sort_type = '_ss' if args.o == 's' else '_ts' if args.o == 't' else ''
    op_file = open(os.path.join(subdir_path, "part_{:03d}".format(part_number) + sort_type + '.' + args.f), 'a')
    if args.f == 'csv':
        write_header(op_file)
    return op_file


def get_signal_data(json_root, signal_key):
    return json_root[signal_key]['data']


def get_sorted_time_keys(json_root):
    time_keys = [[k, v['data'][0]] for k, v in json_root.items() if k.startswith('time')]
    return [k for k, v in sorted(time_keys, key=lambda item: item[1])]


def get_sorted_signal_keys(json_root):
    sig_keys = [[k, len(v['data'])] for k, v in json_root.items() if k.startswith('signal')]
    return sig_keys


def get_line(vals):
    if args.f == 'json':
        return json.dumps({'t': vals[0], 's': vals[1], 'tid': vals[2], 'sid': vals[3]})
    else:
        return ",".join(map(str, vals))


def get_metadata(tk, sk, tf, to, sf, so, u):
    if args.f == 'json':
        return json.dumps(
            {'tid': tk, 'sid': sk, 'time_factor': tf, 'time_offset': to, 'signal_factor': sf, 'signal_offset': so,
             'unit': u})
    else:
        return ",".join(map(str, [tk, sk, tf, to, sf, so, u]))


def write_to_file(file_path, items):
    i = 0
    max_len = len(items)
    out_file_part = 0
    # Create a sub dir to store the parsed results
    sub_out_dir_path = create_subdir(out_dir, file_path)
    out_file = create_outfile(sub_out_dir_path, out_file_part)

    while True:
        lower_limit = i
        upper_limit = max_len if args.n == 0 else min(max_len, i + int(args.n))

        print('Writing: (%d-%d/%d) %f\r' % (lower_limit, upper_limit, max_len, upper_limit * 100 / max_len), end="")
        out_file.write("\n".join([get_line(i) for i in items[lower_limit:upper_limit]]))
        out_file.close()
        out_file_part += 1

        i = upper_limit
        if i == len(items):
            break

        out_file = create_outfile(sub_out_dir_path, out_file_part)


def write_to_kafka(items):
    import confluent_kafka
    conf = {'bootstrap.servers': 'localhost:9092'}
    producer = confluent_kafka.Producer(**conf)
    max_len = len(items)
    print()
    print("Total events:", len(items))
    for i in range(max_len):
        print('Writing: (%d/%d) %f\r' % (i, max_len, i * 100 / max_len), end="")
        producer.produce('sample_1', get_line(items[i]))
        producer.poll(0)
    producer.flush()


def extract_times(file_path):
    print('Extracting times...')
    times = dict()
    with open(file_path) as f:
        items = ijson.kvitems(f, '', use_float=True)
        for k, v in items:
            if k.startswith("time_"):
                times[k] = v
    return times


def extract_data(time_key, times, sig_key, sig):
    time = times[time_key]
    data = []
    for i in range(len(sig['data'])):
        data.append([time['data'][i], sig['data'][i], time_key, sig_key])
    return data


def parse_file_2(file_path):
    times = extract_times(file_path)
    data = []
    print('Processing signals...')
    with open(file_path) as f:
        items = ijson.kvitems(f, '', use_float=True)
        for k, v in items:
            if k.startswith("signal_"):
                print('Processing: %s\r' % k, end="")
                data += (extract_data(v['metadata']['xstr'], times, k, v))
    write_to_file(file_path, data)


def parse_file(file_path):
    items = []
    with open(file_path) as f:
        print('Opening file')
        root = json.load(f)

        metadata_file = 'meta_' + os.path.splitext(os.path.basename(file_path))[0] + '.' + args.f
        metadata_file = open(os.path.join(metadata_dir, metadata_file), 'w+')
        if args.f == 'csv':
            write_metadata_header(metadata_file)

        sig_keys = [k for k in root.keys() if k.startswith('signal')]
        for sig_key in sig_keys:
            print('Processing: %s\r' % sig_key, end="")
            sig_root = root.pop(sig_key, None)
            sig_data = sig_root['data']

            time_key = sig_root['metadata']['xstr']
            time_root = root[time_key]

            metadata_file.write(get_metadata(time_key, sig_key, time_root['metadata']['factor'],
                                             time_root['metadata']['offset'], sig_root['metadata']['factor'],
                                             sig_root['metadata']['offset'], sig_root['metadata']['unit']) + '\n')

            for i in range(len(sig_data)):
                items.append([time_root['data'][i], sig_data[i], time_key, sig_key])

    if args.o != 'none':
        print('\nSorting by', ('time' if args.o == 't' else 'signal'))
        items = sorted(items, key=lambda d: d[0] if args.o == 't' else d[1])

    write_to_file(file_path, items)

    metadata_file.close()


faulthandler.enable()
check_args()
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

if not os.path.exists(metadata_dir):
    os.mkdir(metadata_dir)

path = args.i
if os.path.isfile(path):
    t1 = time.time()
    parse_file_2(path)
    print('Time taken', ((time.time() - t1) * 1000), "ms")
else:
    for file in os.listdir(path):
        if file.endswith('.json'):
            parse_file(os.path.join(path, file))
