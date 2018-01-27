import threading
from stellar_base.address import Address
publickey = 'GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH'
address = Address(address=publickey,network='testnet') # address = Address(address=publickey,network='public') for livenet
def printit():
  threading.Timer(5.0, printit).start()
#  print "Hello, World!"
  address.get() # get the updated information
  print address.balances
printit()




#print "balances: " + address.balances
#print "sequence: " + address.sequence
#print "flags: " + address.flags
#print "signers: " + address.signers
#print "data: " + address.data
# url = 'http://195.201.17.80:8000/accounts/GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH/payments'
