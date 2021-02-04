#! /usr/bin/env python
from __future__ import print_function

"""
RSEM Alignment to transcriptome.
Version: 1.2.0
"""
import sys
import os
import shutil
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed-length', '--seed-length', default='25',
                        help="Seed length used by the read aligner. Providing the correct value is important for RSEM. [default: 25]")
    parser.add_argument('--forward-prob', '--forward-prob', default='0.5',
                        help="Probability of generating a read from the forward strand of a transcript. (Default: 0.5)")
    parser.add_argument('files', nargs='+',
                        help="The file[s] to use.")
    # parser.add_argument('-reference', '--directory', dest='odir', default='.',
    #                        help=
    #                        'Reference base file path with reference name e.g. /home/user/hg_38 '
    #                        '[current directory]')

    return parser.parse_args()


def main():
    # args = parse_args()
    sample_name = "unpaired_genome"
    interim_results_dir = '/mnt/volume/shared/reference-data/'
    rsem_stat = sys.argv[5] + "_rsem_stat"
    rsem_threads = sys.argv[6]
    print(rsem_threads)

    try:
        command = "rsem-calculate-expression -p " + rsem_threads + \
                  " --phred33-quals --seed-length " + sys.argv[1] + \
                  " --forward-prob " + sys.argv[2] + \
                  " --sort-bam-memory-per-thread 2G " \
                  "--time " \
                  "--output-genome-bam " \
                  "--sort-bam-by-coordinate " \
                  "--bowtie2 " + \
                  sys.argv[3] + " " + \
                  interim_results_dir + "ref/" + sys.argv[4] + " " + \
                  sample_name
        os.system(command)
    except Exception as e:
        print('Error while executing rsem-calculate-expression -> %s %s' % command % e)
        sys.exit(1)

    # if os.path.exists(interim_results_dir + rsem_stat):
    #     os.remove(interim_results_dir + rsem_stat)

    if not os.path.exists(interim_results_dir):
        os.mkdir(interim_results_dir)

    try:
        shutil.copy(sample_name + ".stat/" + sample_name + ".cnt", rsem_stat)
    except Exception as e:
        print('Error saving the data in galaxy -> %s' % e)


if __name__ == '__main__':
    main()
    sys.exit(0)
