import threading
import sqlite3
from stellar_base.address import Address
db = sqlite3.connect(':memory:')
watchlist = []
watchlist = ['GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH','GCTAPHEFUDNYUGHUHAIJHMFQURKRKHWJVMER7MSOKK5MTI7RYDOFF5X3']


def checkbalance(publickey):
    address = Address(address=publickey,network='testnet') # address = Address(address=publickey,network='public') for livenet
    address.get() # get the updated information
    balance = address.balances[0]['balance']
    print "balance: for "+ publickey + " "+ balance;
#    checkValue(balance)

#    printword(balance)

def createlocaldb():
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE wallets(id INTEGER PRIMARY KEY, pkey TEXT,
                       balance TEXT, timest TEXT)
    ''')
    db.commit()

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
db.close()

# url = 'http://195.201.17.80:8000/accounts/GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH/payments'
