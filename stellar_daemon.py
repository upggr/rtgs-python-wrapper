import threading
import sqlite3
from stellar_base.address import Address
#db = sqlite3.connect('data/walletsdb',check_same_thread=False)
db = sqlite3.connect(':memory:', check_same_thread=False)
watchlist = []
watchlist = ['GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH','GCTAPHEFUDNYUGHUHAIJHMFQURKRKHWJVMER7MSOKK5MTI7RYDOFF5X3']


def checkbalance(publickey):
    address = Address(address=publickey,network='testnet') # address = Address(address=publickey,network='public') for livenet
    address.get() # get the updated information
    balance = address.balances[0]['balance']
    print "balance: for "+ publickey + " "+ balance;
    logwalletbalance(publickey,balance)
    getbalancechanges()
#    checkValue(balance)

#    printword(balance)

def createlocaldb():
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE wallets(id INTEGER PRIMARY KEY, pkey TEXT,
                       balance TEXT, timest DATETIME DEFAULT CURRENT_TIMESTAMP)
    ''')
    db.commit()

def logwalletbalance(wallet,balance):
    cursor = db.cursor()
    cursor.execute('''INSERT INTO wallets(pkey, balance)
                  VALUES(?,?)''', (wallet,balance))
    print('data in')
    db.commit()

def getbalancechanges():
    cursor = db.cursor()
    cursor.execute('''SELECT pkey, balance FROM wallets''')
    for row in cursor:
    # row[0] returns the first column in the query (name), row[1] returns email column.
        print('{0} : {1}'.format(row[0], row[1]))


def looparray(watchlist):
    for pkey in watchlist:
        checkbalance(pkey);

def printword(theword):
    print theword;

def startchecks():
    threading.Timer(1.0, startchecks).start()
    looparray(watchlist)

createlocaldb()
startchecks();


# url = 'http://195.201.17.80:8000/accounts/GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH/payments'
