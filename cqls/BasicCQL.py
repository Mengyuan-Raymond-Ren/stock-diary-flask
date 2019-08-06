from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

KEYSPACE = "stockdiary"

def createSession() :
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    return session

def createKeySpace(session) :
    session.execute("DROP KEYSPACE IF EXISTS " + KEYSPACE) # TODO: delete this line for release
    print('Create KeySpace...')
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '5' }
        """ % KEYSPACE)

    print('KeySpace Created.')
    session.set_keyspace(KEYSPACE)
    print('KeySpace Set.')
    return session

def dropKeySpace(session) :
    keySpaces = session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
    for keySpace in keySpaces :
        if KEYSPACE == keySpace.keyspace_name:
            print("KeySpace Exists...")
        else :
            print("KeySpace Does Not Exist...")
    
    session.execute("DROP KEYSPACE IF EXISTS " + KEYSPACE)

def createTables(session) :
    session.set_keyspace(KEYSPACE)
    print('Create Table StockOperation...')
    session.execute("""
        CREATE TABLE IF NOT EXISTS StockOperation (
            OperationID uuid,
            TimeCreated text,
            Username text,
            StockCode text,
            StockPrice decimal,
            TradeVolume int,
            TradeType int,
            PRIMARY KEY (OperationID)
        )
        """)
    print('Create Table UserProfile...')
    session.execute("""
        CREATE TABLE IF NOT EXISTS UserProfile (
            UserID int,
            Username text,
            TimeCreated text,
            Status int,
            PRIMARY KEY (UserID)
        )
        """)
    print('Tables Created.')

def operationInsert(session, query, values) :
    session.set_keyspace(KEYSPACE)
    preparedQuery = session.prepare(query)
    print('Query Prepared.')
    feedback = session.execute(preparedQuery.bind(values))
    # feedback = session.execute_async(preparedQuery.bind(values))
    print('Query Executed.')
    return feedback

def operationSelect(session, query) :
    session.set_keyspace(KEYSPACE)
    preparedQuery = session.prepare(query)
    feedback = session.execute(preparedQuery)
    # feedback = session.execute_async(preparedQuery)
    return feedback