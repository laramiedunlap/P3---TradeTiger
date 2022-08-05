pragma solidity ^0.8.0;
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol";

abstract contract TokenPaymentSplitter {
    using SafeERC20 for IERC20;

    address internal paymentToken;
    uint256 internal _totalShares;
    uint256 internal _totalTokenReleased;
    address[] internal _payees;
    mapping(address => uint256) internal _shares;
    mapping(address => uint256) internal _tokenReleased;

    // paymentToken is the address of the ERC20 token we used for payment.

    // _totalShares provides the addition of shares from all payees.

    // _totalTokenReleased is the total amount of payment tokens that have been paid to all recipients.

    // _payees provides an array of all current payee addresses.

    // _shares is the mapping between the address of the payee and the number of shares allocated to them.

    // _tokenReleased is the mapping from the payee address to the number of payment tokens.