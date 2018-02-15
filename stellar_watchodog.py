#!/usr/bin/env python
#title           :stellar_watchodog.py
#description     :Watches an array of addresses (public keys) for changes to their balance.
#author          :Ioannis Kokkinis
#date            :20180215
#version         :0.1
#usage           :python stellar_watchodog.py
#notes           :
#python_version  :2.7
#==============================================================================

import threading
import sqlite3
import requests
import urllib2
import json
from datetime import datetime

# VARIABLES
thenetwork = "http://195.201.17.80:8000" #URL of your node, for example https://horizon-testnet.stellar.org  (no trailing slash)
#thenetwork = "https://horizon-testnet.stellar.org" #URL of your node, for example http://195.201.17.80:8000  (no trailing slash)
stellar_addresses_file = 'stellar_addresses.json' #Point to a remote json file as per stellar_addreses.json example
webhookbaseurl = "http://electronicgr.com/" #Webhook base URL - currently checks only id the url returns 200 to mark the webhook as called.
freq = 3.0 #Update frequency in seconds x.x
logfile = "log.txt" #Log file path.
# END VARIABLES


db = sqlite3.connect(':memory:', check_same_thread=False)

def checkbalance(publickey):
    urlconstruct = thenetwork+'/accounts/'+publickey
    try:
        req = urllib2.Request(urlconstruct)
        handle = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print 'error for wallet : '+publickey+' - %s.' % e.code
        if e.code == 404:
            print 'this wallet does not exist or wallet not synced yet with this node'
        else:
            print 'unknown error contacting the node'
    else:
        opener = urllib2.build_opener()
        f = opener.open(req)
        acctdetails = json.loads(f.read())
        balance = acctdetails['balances'][0]['balance']
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
    cursor.execute('''
    CREATE UNIQUE INDEX uniqness ON webhook_operations(pkey,balance,timest);
    ''')
    db.commit()

def logwalletbalance(wallet,balance):
    cursor = db.cursor()
    cursor.execute('''INSERT OR IGNORE INTO wallets(pkey, balance)
                  VALUES(?,?)''', (wallet,balance))
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
        FileSave(logfile,'[INFO]  '+wallet+' balance update to : '+balance+ ' and webhook at '+webhookbaseurl+' was notified at '+ str(datetime.now()) + ' \n')
    else:
        FileSave(logfile,'[ERROR]  '+wallet+' balance update to : '+balance+ ' and webhook at '+webhookbaseurl+' could NOT be contacted at '+ str(datetime.now()) + ' \n')

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
    threading.Timer(freq, startchecks).start()
    looparray(watchlist)

createlocaltempdbs()
startchecks();
