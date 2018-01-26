var StellarBase = require("stellar-base");
StellarBase.Network.useTestNetwork();

var keypair = StellarBase.Keypair.fromSecret('SBXJ7WZNUGIRG2PTEQEMATWHWMPW73G2WMRQYZ4TNNQTA6OFVPQBA55I');
var account = new StellarBase.Account(keypair.publicKey(), "29799814539509760");

var amount = "100";
var transaction = new StellarBase.TransactionBuilder(account)
  .addOperation(StellarBase.Operation.createAccount({
    destination: StellarBase.Keypair.random().publicKey(),
    startingBalance: amount
  }))
  .build();

transaction.sign(keypair);

console.log(transaction.toEnvelope().toXDR().toString("base64"));