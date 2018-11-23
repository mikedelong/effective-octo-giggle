import logging
from time import time

import numpy as np
import pandas as pd
from pandas.errors import EmptyDataError
from glob import glob
from datetime import datetime
from ntpath import basename

def parse_isd_timestamp(arg):
    return datetime(year=int(arg[0:4]), month=int(arg[4:6]), day=int(arg[6:8]), hour=int(arg[8:10]),
                    minute=int(arg[10:]), second=0, microsecond=0)


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

    output_folder = '../output/'
    input_folder = '../../usca_isd_data/'
    yr_modahrmn = 'YR--MODAHRMN'
    usecols=[yr_modahrmn, 'DIR', 'SPD', 'SKC', 'VSB', 'TEMP', 'DEWP', 'SLP', 'ALT']
    for input_file in glob(input_folder + '*.txt'):
        try:
            short_name = basename(input_file).replace('-2018.isd.txt', '')
            df = pd.read_csv(input_file, delim_whitespace=True, parse_dates=[yr_modahrmn],
                             date_parser=parse_isd_timestamp, na_values=['*', '**', '***', '****', '*****', '******'])
            logger.info('%s %d %s %s' % (short_name, len(df), df[yr_modahrmn].min(), df[yr_modahrmn].max()))
        except EmptyDataError as empty_data_error:
            logger.warning(empty_data_error)

    logger.info('done')

    finish_time = time()
    elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
    elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
    logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
    console_handler.close()
    logger.removeHandler(console_handler)
