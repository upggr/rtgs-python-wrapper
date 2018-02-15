import threading
import sqlite3
import requests
from stellar_base.address import Address
db_pers = sqlite3.connect('data/walletsdb',check_same_thread=False)
db = sqlite3.connect(':memory:', check_same_thread=False)
watchlist = []
watchlist = ['GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH','GCTAPHEFUDNYUGHUHAIJHMFQURKRKHWJVMER7MSOKK5MTI7RYDOFF5X3','GCDR5TNCSR26GV3BR6UYSRE63VZPCTX7GLPFEKZRWFHRUL2GRC6G4Y6R']


def checkbalance(publickey):
    address = Address(address=publickey,network='testnet') # address = Address(address=publickey,network='public') for livenet
    address.get()
    balance = address.balances[0]['balance']
    logwalletbalance(publickey,balance)
    processwebhooks()
    printbalancechanges()

def createlocaltempdbs():
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE if not exists wallets(id INTEGER PRIMARY KEY, pkey TEXT,
                       balance TEXT, timest DATETIME DEFAULT CURRENT_TIMESTAMP)
    ''')
    cursor.execute('''
    CREATE UNIQUE INDEX uniqness ON wallets(pkey,balance);
    ''')
    cursor.execute('''
    CREATE TABLE if not exists webhook_operations(id INTEGER PRIMARY KEY, pkey TEXT,
                       balance TEXT, timest DATETIME DEFAULT CURRENT_TIMESTAMP, webhook_notified INTEGER, webhook_notified_timest DATETIME)
    ''')
    cursor.execute('''
    CREATE TRIGGER create_webhook_record AFTER INSERT ON wallets
    BEGIN
    INSERT OR IGNORE INTO webhook_operations(pkey,balance) VALUES(NEW.pkey,NEW.balance);
    END;
    ''')
    db.commit()

def createlocalpersdb():
    cursor = db_pers.cursor()
    cursor.execute('''
    CREATE TABLE if not exists wallets_balance(id INTEGER PRIMARY KEY, pkey TEXT,
                       balance TEXT, timest DATETIME)
    ''')
    db.commit()

def logwalletbalance(wallet,balance):
    cursor = db.cursor()
    cursor.execute('''INSERT OR IGNORE INTO wallets(pkey, balance)
                  VALUES(?,?)''', (wallet,balance))
    print('data in')
    db.commit()




def processwebhooks():
    cursor = db.cursor()
    cursor.execute('''SELECT pkey, balance, timest FROM webhook_operations where ifnull(length(webhook_notified), 0) = 0''')
    for row in cursor:
            # row[0] returns the first column in the query (name), row[1] returns email column.
        print('{0} : {1} {2}'.format(row[0], row[1], row[2]))
        callwebhook(row[0],row[1])

def callwebhook(wallet,balance):
    print wallet,balance
    r = requests.get("http://electronicgr.com/")
    print r.status_code
    if r.status_code == '400':
        cursor = db.cursor()
        cursor.execute('''UPDATE webhook_operations SET webhook_notified = ?, webhook_notified_timest = CURRENT_TIMESTAMP WHERE pkey = ? AND balance = ?''', ('ok',wallet,balance))
        print('webhook call logged in the database')
        db.commit()
    else:
        print('webhook call will not be logged in the database as it failed')

def printbalancechanges():
    cursor = db.cursor()
#    cursor.execute('''SELECT pkey, balance,timest FROM wallets WHERE timest >= Datetime('now', '-2 seconds')''')
    #cursor.execute('''SELECT pkey, balance, timest FROM wallets''')
    #for row in cursor:
    # row[0] returns the first column in the query (name), row[1] returns email column.
        #print('{0} : {1} {2}'.format(row[0], row[1], row[2]))
    cursor.execute('''SELECT pkey, balance, timest,webhook_notified,webhook_notified_timest FROM webhook_operations''')
    #cursor.execute('''SELECT pkey, balance, timest,webhook_notified,webhook_notified_timest FROM webhook_operations WHERE webhook_notified NOT LIKE 'ok';''')
    for row in cursor:
            # row[0] returns the first column in the query (name), row[1] returns email column.
        print('{0} : {1} {2} {3} {4}'.format(row[0], row[1], row[2], row[3], row[4]))

def looparray(watchlist):
    for pkey in watchlist:
        checkbalance(pkey);

def startchecks():
    threading.Timer(3.0, startchecks).start()
    looparray(watchlist)

createlocaltempdbs()
createlocalpersdb()
startchecks();


# url = 'http://195.201.17.80:8000/accounts/GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH/payments'
