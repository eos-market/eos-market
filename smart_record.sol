// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract NFTWallet {
    struct NFT {
        string chain;  // "EOS" or "ETH"
        address contractAddress;
        uint256 tokenId;
    }

    // Mapping from owner's address to a list of NFTs
    mapping(address => NFT[]) public nfts;

    function addNFT(string memory _chain, address _contractAddress, uint256 _tokenId) public {
        NFT memory newNFT = NFT({
            chain: _chain,
            contractAddress: _contractAddress,
            tokenId: _tokenId
        });
        nfts[msg.sender].push(newNFT);
    }

    function getNFTs(address _owner) public view returns (NFT[] memory) {
        return nfts[_owner];
    }

    // ... other functions to manage or transfer NFTs ...
}
