import argparse
import os
import json
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='Path of the input file')
parser.add_argument('-s', help='Size of the output file', type=str, default='10kb')
parser.add_argument('-n', help='The number of output files', type=int, default=5)
args = parser.parse_args()

sizes = {
    "kb": 1024,
    "mb": 1024 ** 2,
    "gb": 1024 ** 3
}

times = {
    "ms": 1,
    "s": 1000
}


def get_file_name(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]


def get_file_extension(file_path):
    return os.path.splitext(os.path.basename(file_path))[1]


def check_args():
    if not any(args.s.endswith(x) for x in list(sizes.keys()) + list(times.keys())) and not args.s.isnumeric():
        raise ValueError('Error with the split argument')


def get_size():
    s = args.s.replace(" ", "")
    num = int(s[:-2])
    unit = s[-2:]
    return num * sizes[unit]


def get_time():
    s = args.s.replace(" ", "")
    num = int(s[:-1]) if not s.endswith("ms") else int(s[:-2])
    unit = s[-1:] if not s.endswith("ms") else s[-2:]
    return num * times[unit]


def split_by_size(f, size, out_dir):
    file_num = 0
    data = ''
    data_size = 0
    ext = get_file_extension(args.i)
    header = True
    for line in f:
        if ext == '.csv' and header:
            header = False
            continue

        data += line
        data_size += len(line.encode('utf-8'))
        if data_size > size:
            file_name = os.path.join(out_dir, "part_{:03d}".format(file_num) + get_file_extension(args.i))
            write_to_file(file_name, data)
            data = ''
            data_size = 0
            file_num += 1

        if file_num >= args.n:
            break


def split_by_time(f, time, out_dir):
    file_num = 0
    data = ''
    start_time = -1
    ext = get_file_extension(args.i)
    header = True
    for line in f:
        if ext == '.csv' and header:
            header = False
            continue

        if ext == '.json':
            current_time = json.loads(line)['t'] * 1000
        else:
            current_time = float(line.split(',')[0]) * 1000

        if start_time == -1:
            start_time = current_time

        data += line

        if (current_time - start_time) > time:
            file_name = os.path.join(out_dir, "part_{:03d}".format(file_num) + ext)
            write_to_file(file_name, data)
            data = ''
            file_num += 1
            start_time = current_time

        if file_num >= args.n:
            break


def write_to_file(file_path, data):
    fil = open(file_path, 'w+')
    if get_file_extension(args.i) == '.csv':
        fil.write('t,s,tid,sid\n')
    fil.write(data)
    fil.close()


check_args()

is_size_based = any(args.s.endswith(x) for x in ['kb', 'mb', 'gb'])

out_dir = 'out/splits'
tag = 'split_' + args.s + '_'
out_dir = os.path.join(out_dir, tag + get_file_name(args.i))
if os.path.isdir(out_dir):
    shutil.rmtree(out_dir)

os.makedirs(out_dir)

with open(args.i) as f:
    if is_size_based:
        print('Splitting into', args.n, 'files, each with', get_size(), 'kb')
        split_by_size(f, get_size(), out_dir)
    else:
        print('Splitting into', args.n, 'files, each with', get_time(), 'ms')
        split_by_time(f, get_time(), out_dir)

print('Done')
