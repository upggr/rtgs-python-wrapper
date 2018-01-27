from threading import Timer
from time import sleep
from stellar_base.address import Address
publickey = 'GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH'
address = Address(address=publickey,network='testnet') # address = Address(address=publickey,network='public') for livenet


def hello(name):
    print "Hello %s!" % name

print "starting..."
rt = RepeatedTimer(1, hello, "World") # it auto-starts, no need of rt.start()
try:
      address.get() # get the updated information
      balance = str(address.balances)
      print "balance: " + balance
finally:
    rt.stop() # better in a try/finally block to make sure the program ends!




class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.function   = function
        self.interval   = interval
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
#print "balances: " + address.balances
#print "sequence: " + address.sequence
#print "flags: " + address.flags
#print "signers: " + address.signers
#print "data: " + address.data
# url = 'http://195.201.17.80:8000/accounts/GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH/payments'
