import os
import unittest
from interface import ContractInterface
from web3 import HTTPProvider, Web3
import pprint

class TestInterface(unittest.TestCase):

    def setUp(self):

        # Set blockcahin provider
        self.w3 = Web3(HTTPProvider('http://10.10.10.61:7545'))

        self.contract_dir = os.path.abspath('./contracts/')

        self.greeter_interface = ContractInterface(self.w3, 'Greeter', self.contract_dir)


    def test_1_init(self):

        self.assertEqual(
            self.greeter_interface.web3.eth.defaultAccount,
            self.w3.eth.accounts[0],
            'Default account not set correctly'
            )

    def test_2_compile(self):

        self.greeter_interface.compile_source_files()

        self.assertEqual(len(self.greeter_interface.all_compiled_contracts), 3)

    def test_3_deploy(self):

        self.greeter_interface.deploy_contract()

        self.assertTrue(os.path.isfile(self.greeter_interface.deployment_vars_path))

    def test_4_get_instance(self):

        self.greeter_interface.get_instance()

        self.assertEqual(self.greeter_interface.contract_instance.address, self.greeter_interface.contract_address)

    def test_5_change_greeting(self):

        event = 'GreetingChange'
        new_greeting = 'Hola'.encode('utf-8')

        expected_logs = {
            'changer' : self.w3.eth.accounts[0],
            '_from' : 'Hello',
            '_to' : new_greeting,
            'event' : event
        }

        self.greeter_interface.get_instance()
        receipt, indexed_events = self.greeter_interface.send('setGreeting', new_greeting, event=event)

        self.assertTrue(receipt['blockNumber'] > 0)

        self.assertEqual(indexed_events['changer'], expected_logs['changer'], "Logging output for {} inconsistent".format('changer'))
        self.assertEqual(indexed_events['_from'], expected_logs['_from'], "Logging output for {} inconsistent".format('_from'))
        self.assertEqual(indexed_events['changer'], expected_logs['changer'], "Logging output for {} inconsistent".format('changer'))

    def test_6_call_greeting(self):

        expected_greeting = 'Hola'
        # Although the test suite starts with a clean state, the test above
        # changes the contract's greeting on the blockchain, which is what
        # is fetched.

        self.greeter_interface.get_instance()
        actual_greeting = self.greeter_interface.retrieve('greeting')

        self.assertEqual(expected_greeting, actual_greeting, 'Unexpected greeting returned')


if __name__ == '__main__':
    unittest.main()
