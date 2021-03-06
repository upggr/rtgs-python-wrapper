PYTHON WRAPPER FOR RTGS COINS

Installation :

Setup your own node, or use the testnet or public nodes

Edit the variables in stellar_watchdog.py (point to your server, select a webhook address to call when a balance updates, frequency to run, and supply location of the wallets array)

run "python  stellar_watchdog.py"

Inspect the log while you send some lumen to one of the test addresses :)


Stellar Node Setup.
On a new Ubuntu  16.04 machine run :

make sure you can connect using :
ssh root@195.201.17.80 -i ~/.ssh/id_rtgs_rsa   (or your key)

sudo -s
apt-get update
apt-get install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get install docker-ce -y
mkdir stellar


docker run --rm -it -p "8000:8000"  -p "11626:11626"  -p "11625:11625" -p "5432:5432"  -v "/root/stellar:/opt/stellar" --name stellar stellar/quickstart --testnet
take a note of the postgres password ("stellar" in this test server)

docker run -d -p "8000:8000"  -p "11626:11626"  -p "11625:11625" -p "5432:5432" -v "/root/stellar:/opt/stellar" --name stellar stellar/quickstart --testnet

Then edit stellar_watchdog.py variables to point to this node rather than the testnet or public servers


or just run python  stellar_watchdog.py to test it out of the box with 3 sample addresses i control in the testnet, and send some testnet lumen as a test to see the log populating


Youtube demonstration!
---
[![demonstration](https://img.youtube.com/vi/xGE9TObRTAY/0.jpg)](https://youtu.be/xGE9TObRTAY)