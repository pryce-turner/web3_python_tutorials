pragma solidity ^0.5.1;

import "./Owned.sol";

contract Greeter is Owned {
    bytes32 public greeting;

    event GreetingChange (
        address indexed changer,
        bytes32 indexed _from,
        bytes32 indexed _to
    );

    constructor() public {
        greeting = 'Hello';
    }

    function setGreeting(bytes32 _greeting) public onlyBy (owner) {
        emit GreetingChange(msg.sender, greeting, _greeting);
        greeting = _greeting;
    }

    function greet() view public returns (bytes32) {
        return greeting;
    }
}
