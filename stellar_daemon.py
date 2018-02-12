import threading
from stellar_base.address import Address

watchlist = []
watchlist = ['GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH','GCTAPHEFUDNYUGHUHAIJHMFQURKRKHWJVMER7MSOKK5MTI7RYDOFF5X3']
global previousval
previousval = 0
def checkbalance(publickey,previousval):
    address = Address(address=publickey,network='testnet') # address = Address(address=publickey,network='public') for livenet
    address.get() # get the updated information
    balance = address.balances[0]['balance']
    print "balance: for "+ publickey + " "+ balance;
    checkValue(balance,previousval)
#    printword(balance)

def checkValue(val,previousval):
    if previousval == val:
        printword('same')
    else:
        printword('changed')
    previousval = val


def looparray(watchlist):
    for pkey in watchlist:
        checkbalance(pkey);

def printword(theword):
    print theword;

def startchecks():
    threading.Timer(1.0, startchecks).start()
    looparray(watchlist)

startchecks();


# url = 'http://195.201.17.80:8000/accounts/GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH/payments'
