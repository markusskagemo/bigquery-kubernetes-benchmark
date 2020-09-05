from google.cloud import bigquery
import random
import datetime as dt
#import asyncio


def bigquery_service(CRED_PATH='quantum-fusion-233713-5ec9fa7a9e62.json'):
    # Google cloud auth
    return bigquery.Client.from_service_account_json(CRED_PATH)
    

def dummy_streaming_inserts(client, insert_number=10, schema=['DATE', 'TEST'], 
                            dataset_id='netfonds_data', table_id='test'):
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)  # API request

    for _ in range(insert_number):
        # BQ-acceptable now-time str
        ex_dt = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        # To BQ
        rows_to_insert = [
            {schema[0]: ex_dt, schema[1]: chr(random.randint(0, 1000))}
        ]
        # This should be []
        errors = client.insert_rows(table, rows_to_insert)  # API request

    # Return True if 
    return not len(errors)


def dummy_query(client, dataset_id=None, table_id=None, limit=10):
    query_job = client.query("""
    SELECT *
    FROM `quantum-fusion-233713.netfonds_data.test`
    WHERE DATE IS NOT NULL
    ORDER BY DATE DESC
    LIMIT {}""".format(limit))
    results = query_job.result()  # Waits for job to complete.
    
    return results
