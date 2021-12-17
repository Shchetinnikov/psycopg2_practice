from read_json import get_json
import psycopg2

__credentials = get_json('config\\credentials')

conn = psycopg2.connect(database=__credentials['database']['name'],
                        user=__credentials['user']['name'], password=__credentials['user']['password'],
                        host=__credentials['postgres_client']['host'], port=__credentials['postgres_client']['port'])

conn.autocommit = True
