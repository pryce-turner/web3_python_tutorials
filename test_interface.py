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

        self.greeter_interface.compile_source_files()
        self.greeter_interface.deploy_contract()

        self.assertTrue(os.path.isfile(self.greeter_interface.deployment_vars_path))


if __name__ == '__main__':
    unittest.main()
