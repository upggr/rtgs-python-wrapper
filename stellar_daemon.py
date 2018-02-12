import threading
from stellar_base.address import Address

watchlist = []
watchlist = ['GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH','GCTAPHEFUDNYUGHUHAIJHMFQURKRKHWJVMER7MSOKK5MTI7RYDOFF5X3']

def checkbalance(publickey):
    address = Address(address=publickey,network='testnet') # address = Address(address=publickey,network='public') for livenet
    address.get() # get the updated information
    balance = address.balances[0]['balance']
    print "balance: for "+ publickey + " "+ balance;
    setValue(balance)

def setValue(val):
    global globalVal
    valueChanged= globalVal != val
    if valueChanged:
        printword('was')
    globalVal = val
    if valueChanged:
        printword('is')

def looparray(watchlist):
    for pkey in watchlist:
        checkbalance(pkey);

def printword(theword):
    print "Hello, World!" + theword;

def startchecks():
    threading.Timer(1.0, startchecks).start()
    looparray(watchlist)

startchecks();


# url = 'http://195.201.17.80:8000/accounts/GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH/payments'
