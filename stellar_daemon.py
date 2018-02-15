stellar_addresses_file = 'stellar_addresses.json'
webhookbaseurl = "http://electronicgr.com/"


import threading
import sqlite3
import requests
import json
from datetime import datetime
from stellar_base.address import Address
db = sqlite3.connect(':memory:', check_same_thread=False)



#



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
        print('{0} : {1} {2}'.format(row[0], row[1], row[2]))
        callwebhook(row[0],row[1])

def logwebhooktofile(wallet,balance,webhook_notified,time,thetype):
        f = open('data/log.txt', 'a')
        f.write('['+ thetype +']    ['+wallet+'] balance update to : ['+balance+ '] and webhook at ['+webhook_notified+'] was notified at ['+ time + ']')
        f.close()

def FileSave(filename,content):
    with open(filename, "a") as myfile:
        myfile.write(content)

def callwebhook(wallet,balance):
    r = requests.get(webhookbaseurl)
    print r.status_code
    if r.status_code == 200:
        cursor = db.cursor()
        cursor.execute('''UPDATE webhook_operations SET webhook_notified = ?, webhook_notified_timest = CURRENT_TIMESTAMP WHERE pkey = ? AND balance = ?''', (webhookbaseurl,wallet,balance))
        db.commit()
        FileSave('log.txt','[INFO]  '+wallet+' balance update to : '+balance+ ' and webhook at '+webhookbaseurl+' was notified at '+ str(datetime.now()) + ' \n')
    else:
        FileSave('log.txt','[ERROR]  '+wallet+' balance update to : '+balance+ ' and webhook at '+webhookbaseurl+' could NOT be contacted at '+ str(datetime.now()) + ' \n')

def printbalancechanges():
    cursor = db.cursor()
    cursor.execute('''SELECT pkey, balance, timest,webhook_notified,webhook_notified_timest FROM webhook_operations''')
    for row in cursor:
        print('{0} : {1} {2} {3} {4}'.format(row[0], row[1], row[2], row[3], row[4]))

def looparray(watchlist):
    for pkey in watchlist:
        checkbalance(pkey);

def startchecks():
    with open(stellar_addresses_file) as file:
        pkeys = json.load(file)
    watchlist = pkeys['pkeys']
    threading.Timer(3.0, startchecks).start()
    looparray(watchlist)

createlocaltempdbs()
startchecks();


# url = 'http://195.201.17.80:8000/accounts/GCQ2WFN74IOHNRCKS5HWQGM73QVOCYRX5VN53FFQREJDHJ7BM5U7PJCH/payments'
