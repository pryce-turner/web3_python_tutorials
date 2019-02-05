#!/usr/bin/env bash

sudo add-apt-repository ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get upgrade -y

sudo apt-get install -y libssl-dev build-essential automake pkg-config libtool libffi-dev libgmp-dev libyaml-cpp-dev python python3-pip solc

# Install web3 and solc wrapper
pip3 install web3 py-solc-x

# Install node
echo "Run the following in new terminals to finish provisioning"
echo "---------------------------------------------------------"
echo "curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash"
echo "nvm install node"
echo "npm install -g node-gyp truffle ganache-cli"
echo "---------------------------------------------------------"
