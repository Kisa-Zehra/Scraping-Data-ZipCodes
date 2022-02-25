import psycopg2
import configparser


configure = configparser.ConfigParser()
INI_fileName = "config.ini"
configure.read(INI_fileName)
db_port = configure['acl_db']['port']
db_username = 
db_password = 
db_host = 


def qu():
  try:
    conn = None
    conn = pyscopg2.connect(host=db_host,port=db_port, database = acl_db, user=db_username, password=db_password)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE DealersDetails (id serial PRIMARY KEY, name varchar, url varchar, address varchar);")
    cur.execute("INSERT INTO starnow (%s) VALUES (%s)" %(','.join(data), ','.join('%%(%s)s' % k for k in data)), data)
    
    conn.commit()
    cursor.close()
    conn.close()

  except (Exception, psycopg2.DatabaseError) as error:
    print(f"Unable to connect, {error}")

  finally:
    if conn is not None:
      conn.close()
