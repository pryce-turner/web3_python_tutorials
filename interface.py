import os
import pprint
import json

from web3 import Web3, HTTPProvider
from solc import compile_source, compile_files

class ContractInterface(object):

    def __init__(
        self,
        web3,
        contract_to_deploy,
        contract_directory,
        max_deploy_gas = 3000000,
        max_tx_gas = 1000000,
        ):

        self.web3 = web3
        self.contract_to_deploy = contract_to_deploy
        self.contract_directory = contract_directory
        self.deployment_vars_path = os.path.join(os.getcwd(), 'deployment_variables.json')
        self.max_deploy_gas = max_deploy_gas
        self.max_tx_gas = max_tx_gas
        self.web3.eth.defaultAccount = web3.eth.coinbase

    def compile_source_files(self):

        deployment_list = []

        for contract in os.listdir(self.contract_directory):
            deployment_list.append(os.path.join(self.contract_directory, contract))

        self.all_interfaces = compile_files(deployment_list)

        print('Compiled interface keys:\n{}'.format('\n'.join(self.all_interfaces.keys())))

    def deploy_contract(self, **deployment_params):

        try:
            self.all_interfaces is not None
        except ValueError:
            print("Source files not compiled, compiling now and trying again...")

        for interface_key in self.all_interfaces.keys():
            if self.contract_to_deploy in interface_key:
                deployment_interface = self.all_interfaces[interface_key]

                deployment = self.web3.eth.contract(
                    abi=deployment_interface['abi'],
                    bytecode=deployment_interface['bin']
                    )

                deployment_estimate = deployment.constructor().estimateGas(transaction=deployment_params)

                if deployment_estimate < self.max_deploy_gas:
                    tx_hash = deployment.constructor().transact(transaction=deployment_params)

                address = self.web3.eth.waitForTransactionReceipt(tx_hash)['contractAddress']

                print("Deployed {0} to: {1}".format(self.contract_to_deploy, address))

                data = {
                    'contract_address' : self.web3.toChecksumAddress(address),
                    'contract_abi' : deployment_interface['abi']
                }

                with open (self.deployment_vars_path, 'w') as write_file:
                    json.dump(data, write_file, indent=4)

                print('Address and interface ABI for {} written to {}'.format(self.contract_to_deploy, self.deployment_vars_path))

    def get_instance(self):

        with open (self.deployment_vars_path, 'r') as read_file:
            vars = json.load(read_file)

        try:
            address_on_file = vars['contract_address']
        except ValueError("No address found in {}, please call 'deploy_contract' and try again.".format(self.deployment_vars_path)):
            raise

        contract_bytecode_length = len(self.web3.eth.getCode(address_on_file).hex())

        if contract_bytecode_length > 4:
            print('Contract deployed at {}. This function returns an instance object.'.format(address_on_file))
        else:
            print('Contract not deployed at {}.'.format(address_on_file))
            return

        self.contract_instance = self.web3.eth.contract(
            abi = vars['contract_abi'],
            address = vars['contract_address']
        )

        return self.contract_instance

    def send (self, function_, *tx_args, **tx_params):

        fxn_to_call = getattr(self.contract_instance.functions, function_)
        built_fxn = fxn_to_call(*tx_args)

        gas_estimate = built_fxn.estimateGas(transaction=tx_params)
        print("Gas estimate to transact with {}: {}\n".format(function_, gas_estimate))

        if gas_estimate < self.max_tx_gas:

            print("Sending transaction to {} with {} as arguments.\n".format(function_, tx_args))

            tx_hash = built_fxn.transact(transaction=tx_params)

            receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

            print("Transaction receipt mined: \n")
            pprint.pprint(dict(receipt))

        else:
            print("Gas cost exceeds {}".format(self.max_tx_gas))

    def retrieve (self, function_, *call_args):

        fxn_to_call = getattr(self.contract_instance.functions, function_)
        built_fxn = fxn_to_call(*call_args)

        return_values = built_fxn.call()

        return return_values
