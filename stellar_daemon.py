import threading
import sqlite3
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
    getbalancechanges()

def createlocaltempdb():
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE if not exists wallets(id INTEGER PRIMARY KEY, pkey TEXT,
                       balance TEXT, timest DATETIME DEFAULT CURRENT_TIMESTAMP)
    ''')
    cursor.execute('''
    CREATE UNIQUE INDEX uniqness ON wallets(pkey,balance);
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

def getbalancechanges():
    cursor = db.cursor()
#    cursor.execute('''SELECT pkey, balance,timest FROM wallets WHERE timest >= Datetime('now', '-2 seconds')''')
    cursor.execute('''SELECT pkey, balance, timest FROM wallets''')
    for row in cursor:
    # row[0] returns the first column in the query (name), row[1] returns email column.
        print('{0} : {1} {2}'.format(row[0], row[1], row[2]))


def looparray(watchlist):
    for pkey in watchlist:
        checkbalance(pkey);

def printword(theword):
    print theword;

def startchecks():
    threading.Timer(3.0, startchecks).start()
    looparray(watchlist)

createlocaltempdb()
createlocalpersdb()
startchecks();


# url = 'http://195.201.17.80:8000/accounts/GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH/payments'
