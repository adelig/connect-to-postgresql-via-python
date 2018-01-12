from configparser import ConfigParser
import sqlalchemy
import os


def config(filename='credentials.ini', section='postgresql'):
    # Change the directory to the folder where the script itself is located
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)
    
    # Create a parser
    parser = ConfigParser()
    
    # Read config file
    parser.read(filename)
    
    # Get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0].encode('utf-8') ] = param[1].encode('utf-8')
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db



def connect():
    """ Connect to the PostgreSQL database server """
    try:
        # Read connection parameters
        params = config()

        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(params['user'], params['password'], params['host'], \
                int(params['port']), params['database'])

        # Connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        con = sqlalchemy.create_engine(url, client_encoding='utf8')
        print('Connected.')

    except Exception as error:
        print error

    return con


if __name__ == '__main__':

    conn=connect()
    print("\n")

	""" 
	Perform the tasks of your interest
    Like importing a PostgreSQL table as a DataFrame:
	
	import pandas as pd
	df = pd.read_sql_table("table_name",conn)
	"""

    conn.dispose()
    print('Database connection closed.')