import os
from interface import ContractInterface
from web3 import HTTPProvider, Web3

w3 = Web3(HTTPProvider('http://10.10.10.61:7545'))

address = w3.toChecksumAddress('0x92971e17aae84ddf38e880789e01a3239b1eed5d')

event_filt = w3.eth.filter(
    {
        'fromBlock': 'latest',
        'address':address
    }
)

print(dir(event_filt))
