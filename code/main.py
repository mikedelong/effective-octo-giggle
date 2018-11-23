import logging
from time import time

import numpy as np
import pandas as pd
from pandas.errors import EmptyDataError
from glob import glob
from datetime import datetime
from ntpath import basename


def parse_isd_timestamp_hourly(arg):
    return datetime(year=int(arg[0:4]), month=int(arg[4:6]), day=int(arg[6:8]), hour=int(arg[8:10]),
                    minute=0, second=0, microsecond=0)


def parse_isd_timestamp_minutely(arg, arg_minute_flag):
    minute = int(arg[10:])
    return datetime(year=int(arg[0:4]), month=int(arg[4:6]), day=int(arg[6:8]), hour=int(arg[8:10]),
                    minute=minute, second=0, microsecond=0)


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
    usecols = [yr_modahrmn, 'DIR', 'SPD', 'SKC', 'VSB', 'TEMP', 'DEWP', 'SLP', 'ALT']
    usecols = [yr_modahrmn, 'SKC']
    minute_flag = False
    if minute_flag:
        output_file = 'SKC-2018-minutely.csv'
    else:
        output_file = 'SKC-2018-hourly.csv'
    full_output_file = output_folder + output_file
    result_df = None
    count = 0
    na_values = ['*', '**', '***', '****', '*****', '******']
    for input_file in glob(input_folder + '*.txt'):
        try:
            short_name = basename(input_file).replace('-2018.isd.txt', '')
            if minute_flag:
                df = pd.read_csv(input_file, delim_whitespace=True, parse_dates=[yr_modahrmn], usecols=usecols,
                                 date_parser=parse_isd_timestamp_minutely, na_values=na_values)
            else:
                df = pd.read_csv(input_file, delim_whitespace=True, parse_dates=[yr_modahrmn], usecols=usecols,
                                 date_parser=parse_isd_timestamp_hourly, na_values=na_values)
            logger.info('%s %d %s %s' % (short_name, len(df), df[yr_modahrmn].min(), df[yr_modahrmn].max()))
            if result_df is None:
                result_df = df[[yr_modahrmn, 'SKC']].rename(columns={'SKC': short_name})
            else:
                result_df = result_df.merge(df[[yr_modahrmn, 'SKC']].rename(columns={'SKC': short_name}),
                                            on=yr_modahrmn, how='outer')
                result_df = result_df.drop_duplicates(subset=list(result_df)[:-1], keep='last')
                logger.info('after join %d rows and %d columns' % (len(result_df), len(list(result_df))))
                if count % 10 == 5:
                    logger.info('writing result to %s' % full_output_file)
                    result_df.to_csv(full_output_file, index=False)
                count += 1
        except EmptyDataError as empty_data_error:
            logger.warning(empty_data_error)
    logger.info('after final join %d rows and %d columns' % (len(result_df), len(list(result_df))))
    logger.info('writing result to %s' % full_output_file)
    result_df.to_csv(full_output_file, index=False)

    logger.info('done')

    finish_time = time()
    elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
    elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
    logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
    console_handler.close()
    logger.removeHandler(console_handler)
