pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract NFT is ERC721Enumerable, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;

    constructor() ERC721("eosmarketNFT", "MNFT") {}

    function mint(address recipient) external onlyOwner {
        _tokenIdCounter.increment();
        _safeMint(recipient, _tokenIdCounter.current());
    }

    function trade(uint256 tokenId, address to) external {
        require(ownerOf(tokenId) == msg.sender, "Not the owner");
        _transfer(msg.sender, to, tokenId);
    }
}
