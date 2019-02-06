pragma solidity ^0.5.1;

contract Emitter {

    event SendIt (
        bool indexed _bool,
        int indexed _int,
        bytes32 indexed _bytes32
    );

    function fullSend () public {
        emit SendIt(true, 69, "Eyo");
    }
}
