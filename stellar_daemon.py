import schedule
import time
from stellar_base.address import Address
publickey = 'GCTAPHEFUDNYUGHUHAIJHMFQURKRKHWJVMER7MSOKK5MTI7RYDOFF5X3'


def checkbalance(publickey):
    address = Address(address=publickey,network='testnet') # address = Address(address=publickey,network='public') for livenet
    address.get() # get the updated information
    balance = address.balances[0]['balance']
#    balance = str(address.balances)
    print "balance: for "+ publickey + " "+ balance;

#schedule.every(2).seconds.do(job)
#while 1:
#   schedule.run_pending()
#   time.sleep(1)
checkbalance(publickey);





#print "balances: " + address.balances
#print "sequence: " + address.sequence
#print "flags: " + address.flags
#print "signers: " + address.signers
#print "data: " + address.data
# url = 'http://195.201.17.80:8000/accounts/GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH/payments'
