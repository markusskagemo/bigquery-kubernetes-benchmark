import utils
import logging
import time
import datetime as dt
import pandas as pd
import argparse
import subprocess
import numpy as np
import requests as r

    
if __name__ == '__main__':
    # Parse cl arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--inserts', type=int, default=10, help='Amount of rows to insert per loop.')
    ap.add_argument('-p', '--passes', type=int, default=5, help='Amount of times to loop query and insert jobs.')
    ap.add_argument('-ql', '--querylimit', type=int, default=20, help='Max rows in query response.')
    ap.add_argument('--host', type=str, default='https://www.iltalehti.fi/robots.txt', help='Ping destination.')
    ap = ap.parse_args()
    
    # Init logging
    logging.basicConfig(level=logging.DEBUG)
    # Get BQ client
    client = utils.bigquery_service()
    # Dict for df conversion
    timing = {'time': [], 'mean insert time': [], 'query time': [], 'ping': []}
    for i in range(ap.passes):
        # Ping host
        pingtimes = []
        for _ in range(5):
            t0 = time.time()
            r.get(ap.host)
            pingtimes.append(time.time() - t0)
        pingtimes = np.array(pingtimes)
        timing['ping'].append(np.median(pingtimes))
        
        # Current time
        timing['time'].append(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        
        # Inserts
        t0 = time.time()
        utils.dummy_streaming_inserts(client, insert_number=ap.inserts)
        mu_inserts = (time.time() - t0)/ap.inserts
        timing['mean insert time'].append(mu_inserts)
        logging.debug('mean insert time: {}'.format(mu_inserts))
        
        # Querying
        t0 = time.time()
        utils.dummy_query(client, limit=ap.querylimit)
        query_time = time.time() - t0
        timing['query time'].append(query_time)
        logging.debug('query time: {}'.format(query_time))
        
    timing_df = pd.DataFrame.from_dict(timing)
    timing_df.to_csv('times.csv')

    # To benchmark table on BQ
    table_ref = client.dataset('logging').table('benchmark')
    table = client.get_table(table_ref)  # API request
    
    for i in range(len(timing_df['time'])):
        # To BQ
        rows_to_insert = [
            {'time': timing_df.loc[i, 'time'],
            'mean_insert_time': timing_df.loc[i, 'mean insert time'],
            'ping': timing_df.loc[i, 'ping'],
            'query_time': timing_df.loc[i, 'query time']}
        ]
        # This should be []
        errors = client.insert_rows(table, rows_to_insert)  # API request