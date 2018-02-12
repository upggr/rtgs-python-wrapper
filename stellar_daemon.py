import schedule
import threading
import time
from stellar_base.address import Address
watchlist = []
watchlist = ['GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH','GCTAPHEFUDNYUGHUHAIJHMFQURKRKHWJVMER7MSOKK5MTI7RYDOFF5X3']
#publickey = 'GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH,GCTAPHEFUDNYUGHUHAIJHMFQURKRKHWJVMER7MSOKK5MTI7RYDOFF5X3'


def checkbalance(publickey):
    address = Address(address=publickey,network='testnet') # address = Address(address=publickey,network='public') for livenet
    address.get() # get the updated information
    balance = address.balances[0]['balance']
#    balance = str(address.balances)
    print "balance: for "+ publickey + " "+ balance;

def looparray(watchlist):
    for pkey in watchlist:
        checkbalance(pkey);

#looparray(watchlist)
#schedule.every(2).seconds.do(looparray(watchlist))
#while 1:
#   schedule.run_pending()
#   time.sleep(1)
def printword():
    print "Hello, World!";

def startchecks():
    threading.Timer(1.0, startchecks).start()
    printword()
#    print "Hello, World!"

startchecks(watchlist);


#print "balances: " + address.balances
#print "sequence: " + address.sequence
#print "flags: " + address.flags
#print "signers: " + address.signers
#print "data: " + address.data
# url = 'http://195.201.17.80:8000/accounts/GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH/payments'
