# Testing `datacarriersize` applies to total `OP_RETURN` data

1. first need to use v30 with patch to allow for multiple `OP_RETURN`s to be created in `createrawtransaction` which can be found at https://github.com/xstoicunicornx/bitcoin in `master` branch (for simplicity and out of laziness just used bitcoin core `master` branch as of 2025/10/04)

2. use the 'Preparation' section in [Bitcoin Core v30 Testing Guide](https://github.com/bitcoin-core/bitcoin-devwiki/wiki/30.0-Release-Candidate-Testing-Guide) to set up relavant v30 variables/aliases

3. setup the test scenario with `datacarriersize` is set to 83
```bash
echo "regtest=1" > $DATA_DIR_30/bitcoin.conf
bitcoind30 -daemon -datacarriersize=83
bcli30 createwallet "satoshi"   
bcli30 generatetoaddress 101 $(bcli30 getnewaddress)
coinbase_txid=$(bcli30 listunspent | jq -r ".[0].txid")
```
3. test that single `OP_RETURN` of just under 83 bytes is valid
```bash
satoshi_address=$(bcli30 getnewaddress)
tx_opreturn=$(bcli30 createrawtransaction "[{\"txid\":\"$coinbase_txid\",\"vout\":0}]" \
    "[{\"$satoshi_address\":49.99990000},{\"data\":\"6a4d50c3ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\"}]")
tx_op_return_signed=$(bcli30 signrawtransactionwithwallet $tx_opreturn | jq -r .hex)
bcli30 testmempoolaccept "[\"$tx_op_return_signed\"]"
```
4. test that multiple `OP_RETURN` of just under 83 bytes is invalid
```bash
satoshi_address=$(bcli30 getnewaddress)
tx_opreturn=$(bcli30 createrawtransaction "[{\"txid\":\"$coinbase_txid\",\"vout\":0}]" \
    "[{\"$satoshi_address\":49.99990000},{\"data\":\"6a4d50c3ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\"},{\"data\":\"6a4d50c3ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\"}]")
tx_op_return_signed=$(bcli30 signrawtransactionwithwallet $tx_opreturn | jq -r .hex)
bcli30 testmempoolaccept "[\"$tx_op_return_signed\"]"
```
