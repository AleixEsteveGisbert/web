// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HostCoinSale {
    mapping(address => uint) public balances;
    uint public tokenPrice;
    address public owner;

    event TokensPurchased(address buyer, uint amount);
    event TokensSpent(address spender, uint amount);

    constructor(uint _tokenPrice) {
        tokenPrice = _tokenPrice;
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    function buyTokens(uint _amount) external payable {
        uint totalCost = tokenPrice * _amount;
        require(msg.value >= totalCost, "Insufficient Ether");

        balances[msg.sender] += _amount;
        emit TokensPurchased(msg.sender, _amount);
    }

    function spendTokens(uint _amount) public {
        require(balances[msg.sender] >= _amount, "Insufficient balance");

        balances[msg.sender] -= _amount;
        emit TokensSpent(msg.sender, _amount);
    }

    receive() external payable {}

    function withdrawFunds() external onlyOwner {
        payable(owner).transfer(address(this).balance);
    }
}
