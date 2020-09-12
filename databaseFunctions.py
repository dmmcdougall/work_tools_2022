'''

'''

# standard library
import pyodbc

# third part libraries
import config as cfg

# local repo

# find the number we need to start the new data with
def find_next_row_from_db(my_table):
    query = "SELECT * FROM " + table
    df_hShift = pd.read_sql(query, cfg.conn)
    last_shift = df_hShift[my_table].max()
    # print(last_shift) # for testing
    new_shift = last_shift + 1
    return new_shift


# read from SQL and print to screen
def read2screen(query, conn):
    print("Read Method")
    cursor = conn.cursor()
    cursor.execute(query)
    for row in cursor:
        print(row)


# read from SQL without printing
def read2(query, conn):
    print("Read Method")
    cursor = conn.cursor()
    cursor.execute(query)

# general method
def general(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)

# does your table exist?
def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

def drop_table(self, table):
    self._exec(schema.DropTable(table))

if __name__ == '__main__':
    print()
    print('------------')
    print("METHOD CHECK")
    print('------------')
    print()
    query = "SELECT * FROM sys.tables"
    read(query, cfg.conn)


