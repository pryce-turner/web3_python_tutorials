pragma solidity ^0.5.1;

contract Owned {

    address payable public owner = msg.sender;
    uint public creationBlock = block.number;

    modifier onlyBy (address _account) {
        require(msg.sender == _account);
        _;
    }

    function changeOwner (address payable _newOwner) public onlyBy (owner) {
        owner = _newOwner;
    }

    function destroy() public onlyBy (owner) {
        selfdestruct(owner);
    }
}
