import logging
from time import time

import numpy as np
import pandas as pd

if __name__ == '__main__':
    start_time = time()

    console_formatter = logging.Formatter('%(asctime)s : %(name)s :: %(levelname)s : %(message)s')
    file_formatter = logging.Formatter('%(asctime)s : %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    logger.info('started')

    input_folder = '../data/'
    input_file = 'superghcnd_full_20181007.csv.gz'
    full_input_file = input_folder + input_file
    logger.info('reading data from input file %s' % full_input_file)
    output_folder = '../output/'

    usecols = None
    nrows = 100
    compression = 'gzip'
    df = pd.read_csv(full_input_file, sep=',', usecols=usecols, nrows=nrows, compression=compression)
    logger.info(list(df))
    logger.info(df.shape)
    logger.info(df.head())

    logger.info('done')

    finish_time = time()
    elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
    elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
    logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
    console_handler.close()
    logger.removeHandler(console_handler)
