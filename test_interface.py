import os
import unittest
from interface import ContractInterface
from web3 import HTTPProvider, Web3

class TestInterface(unittest.TestCase):

    def setUp(self):

        # Set blockcahin provider
        self.w3 = Web3(HTTPProvider('http://10.10.10.61:7545'))

        self.contract_dir = os.path.abspath('./contracts/')

        self.greeter_interface = ContractInterface(self.w3, 'Greeter', self.contract_dir)


    def test_init(self):

        self.assertEqual(
            self.greeter_interface.web3.eth.defaultAccount,
            self.w3.eth.accounts[0],
            'Default account not set correctly'
            )

    def test_compile(self):

        self.greeter_interface.compile_source_files()

        self.assertEqual(len(self.greeter_interface.all_interfaces), 2)

    def test_deploy(self):

        self.greeter_interface.deploy_contract()

        self.assertTrue(os.path.isfile(self.greeter_interface.deployment_vars_path))

    def test_get_instance(self):

        self.greeter_interface.get_instance()

        self.assertEqual(self.greeter_interface.contract_instance.address, self.greeter_interface.contract_address)

    def test_change_greeting(self):

        event = 'GreetingChange'
        new_greeting = 'Sup?'

        expected_logs = {
            'changer' : w3.eth.accounts[0],
            'from' : 'Hello',
            '_to' : new_greeting,
            'event' : event
        }

        self.greeter_interface.get_instance()
        receipt, tx_logs = self.greeter_interface.send('setGreeting', new_greeting, event=event)

        self.assertTrue(receipt['blockNumber'] > 0)

        for key, value in expected_logs.items():
            self.assertEqual(tx_logs[key], expected_logs[key], "Logging output for {} inconsistent".format(key))


if __name__ == '__main__':
    unittest.main()
