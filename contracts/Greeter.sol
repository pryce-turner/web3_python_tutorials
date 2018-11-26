pragma solidity ^0.4.25;

import "./Owned.sol";

contract Greeter is Owned {
    string public greeting;

    constructor() public {
        greeting = 'Hello';
    }

    function setGreeting(string _greeting) public onlyBy (owner) {
        greeting = _greeting;
    }

    function greet() view public returns (string) {
        return greeting;
    }
}
