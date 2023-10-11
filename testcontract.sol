// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";

contract ComplexERC721 is ERC721Enumerable, Ownable, Pausable, ERC721Burnable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;
    
    // Rate limiting: Only one mint every 5 minutes per address
    mapping(address => uint256) private _lastMintTimestamp;
    uint256 constant MINT_RATE_LIMIT = 5 minutes;

    constructor() ERC721("ComplexNFT", "CNFT") {}

    function mint(address recipient, string memory tokenURI) external whenNotPaused {
        require(_canMint(msg.sender), "Minting rate exceeded");
        
        _tokenIdCounter.increment();
        uint256 newTokenId = _tokenIdCounter.current();
        _safeMint(recipient, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        
        _updateMintTimestamp(msg.sender);
    }

    function pause() external onlyOwner {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
    }
    
    function _canMint(address account) internal view returns (bool) {
        return block.timestamp - _lastMintTimestamp[account] > MINT_RATE_LIMIT;
    }

    function _updateMintTimestamp(address account) internal {
        _lastMintTimestamp[account] = block.timestamp;
    }
}
