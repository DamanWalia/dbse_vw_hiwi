# VW Data Parser

## Usage

To run the script just call `python parser.py -i file_name.json -n 0 -f csv` with the listed commandline arguments

### Commandline arguments

- **-i** for specifying the input. Can be a file or a folder
- **-n** for specifying how many signal entries an output file should contain. Default is 10^6. Set to 0 for no splitting.
- **-f** for specifying the output format of the data. Can be `json` or `csv`
