// SPDX-License-Identifier: MIT

pragma solidity >=0.6.6;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol"; // This import this changed from ERC721 due to _setTokenURI not being present in ERC721.
import "@chainlink/contracts/src/v0.8/interfaces/LinkTokenInterface.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

contract AdvancedCollectible is ERC721URIStorage, VRFConsumerBaseV2 {
    uint16 requestConfirmations = 3;
    
    uint32 callbackGasLimit = 200000;
    uint32 numWords = 1;

    uint64 public subscriptionId;

    bytes32 public keyHash;

    uint256 public tokenCounter;
    uint256 public _requestId;
    uint256[] _randomWords;

    address owner;


    enum PPTYPE {
        AVERAGE_HAIRY_CIRCUM,
        AVERAGE_CLEAN_CIRCUM,
        AVERAGE_HAIRY_UNCIRCUM,
        AVERAGE_CLEAN_UNCIRCUM,
        SHORT_HAIRY_UNCIRCUM,
        SHORT_CLEAN_UNCIRCUM,
        SHORT_HAIRY_CIRCUM,
        SHORT_CLEAN_CIRCUM,
        HUGE_HAIRY_CIRCUM,
        HUGE_CLEAN_CIRCUM,
        HUGE_HAIRY_UNCIRCUM,
        HUGE_CLEAN_UNCIRCUM
    }

    mapping(uint256 => uint256) public tokenIdToPP;
    mapping(uint256 => address) public requestIDToSender;

    event requestedCollectible(uint256 indexed _requestId, address requester);
    event ppAssigned(uint256 indexed tokenId, PPTYPE pp);
    event ReturnedRandomness(uint256[] _randomWords);

    VRFCoordinatorV2Interface immutable coordinator;
    LinkTokenInterface immutable linktoken;

    constructor(address _VRFCoordinator,address _link,uint64 _subId, bytes32 _keyHash) public VRFConsumerBaseV2(_VRFCoordinator) ERC721("PeePeeProject", "PP") {
        coordinator = VRFCoordinatorV2Interface(_VRFCoordinator);
        linktoken = LinkTokenInterface(_link);

        owner = msg.sender;

        tokenCounter = 0;
        subscriptionId = _subId;
        keyHash = _keyHash;
    }


    function createCollectible() public returns (bytes32) {
        _requestId = coordinator.requestRandomWords(keyHash, subscriptionId, requestConfirmations, callbackGasLimit, numWords);
        requestIDToSender[_requestId] = msg.sender;
        emit requestedCollectible(_requestId, msg.sender);
    }


    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function fulfillRandomWords(uint256 requestId, uint256[] memory randomWords) internal override
    {
        uint256 calc = randomWords[0] % 12;
        PPTYPE pptype = PPTYPE(calc);
        uint256 newTokenId = tokenCounter;

        tokenIdToPP[newTokenId] = calc;
        

        emit ppAssigned(newTokenId, pptype);

        address _owner = requestIDToSender[requestId];
        _safeMint(_owner, newTokenId);

        tokenCounter += 1;

        _randomWords = randomWords;
        
        emit ReturnedRandomness(randomWords);
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: The caller is not owner or approved."
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
