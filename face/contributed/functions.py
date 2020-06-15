# https://www.postgresqltutorial.com/postgresql-python/transaction/
#!/usr/bin/python
import psycopg2
from config import config



def connect(): # 접속되면 버전확인 하는 함수
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	    # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')



def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE customers (
            customer_id SERIAL PRIMARY KEY,
            customer_name VARCHAR(255) NULL,
            customer_age VARCHAR(255) NOT NULL,
            customer_gender VARCHAR(255) NOT NULL,
            customer_phone VARCHAR(255) NULL
        )
        """,
        """ CREATE TABLE items (
                item_id SERIAL PRIMARY KEY,
                item_producer VARCHAR(255) NULL,
                item_group VARCHAR(255) NULL,
                item_price VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE customer_pics (
                customer_id INTEGER PRIMARY KEY,
                file_extension VARCHAR(5) NOT NULL,
                pic_data BYTEA NOT NULL,
                FOREIGN KEY (customer_id)
                REFERENCES customers (customer_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE customer_items (
                customer_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                PRIMARY KEY (customer_id , item_id),
                FOREIGN KEY (customer_id)
                    REFERENCES customers (customer_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (item_id)
                    REFERENCES items (item_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



def sequences():
    sql = """SELECT sequence_schema, sequence_name
	            FROM information_schema.sequences;"""
    conn = None
    customer_id = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        tmp = cur.fetchall()
        # conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('='*25, '시퀸스목록', '='*25, '\n', tmp, '\n', '='*60)



def insert_customer(customer_age, customer_gender):
    """ insert a new customer into the customers table """
    sql = """INSERT INTO customers(customer_age, customer_gender)
             VALUES(%s,%s) RETURNING customer_id;"""
    conn = None
    customer_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (customer_age, customer_gender))
        # get the generated id back
        customer_id = cur.fetchone()[0]
        print('추가', customer_id)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return customer_id



def update_customer(customer_id, customer_age, customer_gender):
    """ update customer info based on the customer id """
    sql = """ UPDATE customers
                SET (customer_age, customer_gender) = (%s,%s)
                WHERE customer_id = %s"""
    conn = None
    updated_rows = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql, (customer_age, customer_gender, customer_id))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows



def insert_customer_list(customer_list):
    """ insert multiple customers into the customers table  """
    sql = "INSERT INTO customers(customer_age, customer_gender) VALUES(%s,%s)"
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql,customer_list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



def add_item(item_name, customer_list):
    # statement for inserting a new row into the items table
    insert_item = """INSERT INTO items(item_name, item_producer, item_group, item_price) 
                    VALUES(%s,%s,%s,%s) RETURNING item_id;"""
    # statement for inserting a new row into the customer_items table
    assign_customer = "INSERT INTO customer_items(customer_id,item_id) VALUES(%s,%s)"

    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # insert a new item
        cur.execute(insert_item, (item_name, item_producer, item_group, item_price))
        # get the item id
        item_id = cur.fetchone()[0]
        # assign items provided by customers
        for customer_id in customer_list:
            cur.execute(assign_customer, (customer_id, item_id))

        # commit changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



def get_items(customer_id):
    """ get items provided by a customer specified by the customer_id """
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a cursor object for execution
        cur = conn.cursor()
        # another way to call a stored procedure
        # cur.execute("SELECT * FROM get_items_by_customer( %s); ",(customer_id,))
        cur.callproc('get_items_by_customer', (customer_id,))
        # process the result set
        row = cur.fetchone()
        while row is not None:
            print(row)
            row = cur.fetchone()
        # close the communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



# https://www.postgresqltutorial.com/postgresql-python/blob/
def write_blob(customer_id, path_to_file, file_extension):
    """ insert a BLOB into a table """
    conn = None
    try:
        # read data from a picture
        pic = open(path_to_file, 'rb').read()
        # read database configuration
        params = config()
        # connect to the PostgresQL database
        conn = psycopg2.connect(**params)
        # create a new cursor object
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute("INSERT INTO customer_pics(customer_id,file_extension,pic_data) " +
                    "VALUES(%s,%s,%s)",
                    (customer_id, file_extension, psycopg2.Binary(pic)))
        # commit the changes to the database
        conn.commit()
        # close the communication with the PostgresQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



def read_blob(customer_id, path_to_dir):
    """ read BLOB data from a table """
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgresQL database
        conn = psycopg2.connect(**params)
        # create a new cursor object
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(""" SELECT customer_age, file_extension, pic_data
                        FROM customer_pics
                        INNER JOIN customers on customers.customer_id = customer_pics.customer_id
                        WHERE customers.customer_id = %s """,
                    (customer_id,))

        blob = cur.fetchone()
        open(path_to_dir + blob[0] + '.' + blob[1], 'wb').write(blob[2])
        # close the communication with the PostgresQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



if __name__ == '__main__':
   connect() # 버전확인
