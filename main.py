from bitcoin import SelectParams
from bitcoin.core.script import OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG

from extra import create_OP_CHECKSIG_signature, create_txout, create_txin, create_signed_transaction, broadcast_transaction
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.wallet import CBitcoinAddress

def P2PKH_scriptPubKey(address):
    return [OP_DUP, OP_HASH160, address, OP_EQUALVERIFY, OP_CHECKSIG]


def P2PKH_scriptSig(txin, txout, txin_scriptPubKey, private_key, public_key):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey,
                                             private_key)
    return [signature, public_key]


def send_from_P2PKH_transaction(amount_to_send,
                                txid_to_spend,
                                utxo_index,
                                txout_scriptPubKey,
                                sender_private_key,
                                network):

    sender_public_key = sender_private_key.pub
    sender_address = P2PKHBitcoinAddress.from_pubkey(sender_public_key)

    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_scriptPubKey(sender_address)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey,
        sender_private_key, sender_public_key)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx, network)


if __name__ == '__main__':
    SelectParams('testnet')

    ######################################################################
    #

    my_private_key = CBitcoinSecret('cSSyMMZQkB4uLULkEAF4CypPF2meKrwfox2sXz6BEnmMLckc4Y9E')

    my_public_key = my_private_key.pub
    my_address = P2PKHBitcoinAddress.from_pubkey(my_public_key)

    faucet_address = CBitcoinAddress('mr2gt3V9KiBmaPsJTtWxqjaHkXcX46Nrjt')
    amount_to_send = 0.001
    txid_to_spend = (
        'c5cbb8836612144a69f33775810a725b715140608093e902b609f28f7ff90457')
    utxo_index = 0
    network = 'btc-test3'

    #
    ######################################################################

    txout_scriptPubKey = P2PKH_scriptPubKey(faucet_address)
    response = send_from_P2PKH_transaction(
        amount_to_send,
        txid_to_spend,
        utxo_index,
        txout_scriptPubKey,
        my_private_key,
        network,
    )
    print(response.status_code, response.reason)
    print(response.text)