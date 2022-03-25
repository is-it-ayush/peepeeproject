// SPDX-License-Identifier: MIT

pragma solidity >=0.6.6;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol"; // This import this changed from ERC721 due to _setTokenURI not being present in ERC721.

contract SimpleCollectible is ERC721URIStorage {

    // This keeps a track of total tokens
    uint256 public tokenCounter;

    // Inheriting from ERC721 so basically we need to give a name and a symbol. 
    constructor () public ERC721("PeePeeProject","PP") {
      
        //  When the contract is deployed, the counter will be set to 0.
        tokenCounter = 0;
    }

    // Creating a nft.
    function createCollectible(string memory tokenURI) public returns (uint256) {
       
        // Creating a token id which will be equal to the token count.
        uint256 newTokenId = tokenCounter;
       
        // Calling the _safeMint function from ERC721 Contract.
        // _safeMint: It's just a mint function but with a few safety checks.
        _safeMint(msg.sender, newTokenId);

        _setTokenURI(newTokenId, tokenURI);

        // Increment tokenCounter by 1
        tokenCounter+=1;

        // Return the token Id
        return newTokenId;
    }

}