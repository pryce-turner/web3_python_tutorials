pragma solidity ^0.4.25;

import "./Owned.sol";

contract Greeter is Owned {
    string public greeting;

    event GreetingChange (
      address indexed changer,
      string indexed _from,
      string indexed _to
    );

    constructor() public {
        greeting = 'Hello';
    }

    function setGreeting(string _greeting) public onlyBy (owner) {
        emit GreetingChange(msg.sender, greeting, _greeting);
        greeting = _greeting;
    }

    function greet() view public returns (string) {
        return greeting;
    }
}
