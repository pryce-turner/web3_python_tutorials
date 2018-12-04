import os
from interface import ContractInterface
from web3 import HTTPProvider, Web3

w3 = Web3(HTTPProvider('http://10.10.10.61:7545'))
contract_dir = os.path.abspath('./contracts/')
greeter_interface = ContractInterface(w3, 'Greeter', contract_dir)

greeter_interface.compile_source_files()
greeter_interface.deploy_contract()
greeter_interface.get_instance()

address = greeter_interface.contract_address

greetings = [
    'Hey',
    'Hows it?',
    'Ello?',
    'Yo'
]

greeter_interface.send('setGreeting', 'Hey', event='GreetingChange')

# for greeting in greetings:
#     greeter_interface.send('setGreeting', greeting)
#
# event_filt = w3.eth.filter(
#     {
#         'address': address,
#         'fromBlock': 0,
#         'toBlock': 'latest'
#     }
# )
#
# print(greeter_interface.contract_address)
# print(event_filt)
# print(event_filt.get_new_entries())
