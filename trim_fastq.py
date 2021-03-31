#!/usr/bin/env python

from __future__ import print_function
from __future__ import unicode_literals
import sys
import argparse
from collections import namedtuple

def get_opts():
    """Extract program options
    """
    parser = argparse.ArgumentParser(description=__doc__,
                            usage="{0} -h [options] [arg]".format(sys.argv[0]))

    parser.add_argument('-i', '--input-fastq-files', 
            dest='input_fastq_files', nargs='+', type=argparse.FileType('r'), default=[sys.stdin], 
            help='Fastq files to process')  

    parser.add_argument('-o', '--output-fastq-file', 
            dest='output_fastq_file', type=argparse.FileType('w'), default=sys.stdout, 
            help='Output fastq file')  

    parser.add_argument('--min-length', 
            dest='min_length', type=int, default=0, 
            help='Reject the reads whose length is lower than this value')  

    parser.add_argument('--max-length',
            dest='max_length', type=int, default=sys.maxint,
            help='Trim the reads whose length exceed this value')  

    return parser.parse_args()


FastqEntry=namedtuple('FastqEntry', ['seq_id', 'seq_len', 'seq', 'qual'])
def fastq_reader(istream):
    while istream:
        seq_id = istream.next().rstrip('\n')
        seq = istream.next().rstrip('\n')
        istream.next()
        qual = istream.next().rstrip('\n')
        yield FastqEntry(seq_id, len(seq), seq, qual)

def fastq_format(fastq_entry, max_length):
    return '{0}\n{1}\n+\n{2}'.format(
            fastq_entry.seq_id,
            fastq_entry.seq[0:min(fastq_entry.seq_len, max_length)],
            fastq_entry.qual[0:min(fastq_entry.seq_len, max_length)])

def main():
    opts = get_opts()
    for input_fastq_file in opts.input_fastq_files:
        for fastq_entry in fastq_reader(input_fastq_file):
            seq_len = len(fastq_entry.seq)
            if seq_len >= opts.min_length:
                print(fastq_format(fastq_entry, opts.max_length), file=opts.output_fastq_file)

if __name__ == '__main__':
    main()
