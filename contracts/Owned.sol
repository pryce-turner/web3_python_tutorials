pragma solidity ^0.4.25;

contract Owned {

    address public owner = msg.sender;
    uint public creationBlock = block.number;

    modifier onlyBy (address _account) {
        require(msg.sender == _account);
        _;
    }

    function changeOwner (address _newOwner) public onlyBy (owner) {
        owner = _newOwner;
    }

    function destroy() public onlyBy (owner) {
        selfdestruct(owner);
    }
}
