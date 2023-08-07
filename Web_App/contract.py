from web3 import Web3

from web3 import Web3

alchemy_url = "https://eth-sepolia.g.alchemy.com/v2/5APA3WpSw2ESkV84Qlcy-4ZgFQW9I9_M"
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# Dirección de tu contrato inteligente
contract_address = "0x0Ff0705efe9fb8A300047A365f39BEFfA86D7c6f"

# ABI (Interfaz de Contrato ABI) del contrato inteligente
contract_abi = contractAbi = [
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_tokenPrice",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "buyer",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "TokensPurchased",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "TokensSpent",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "balances",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            }
        ],
        "name": "buyTokens",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            }
        ],
        "name": "spendTokens",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "tokenPrice",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "withdrawFunds",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "stateMutability": "payable",
        "type": "receive"
    }
]


def get_wallet_address():
    if hasattr(Web3, 'ethereum') and Web3.ethereum.is_connected():
        try:
            accounts = Web3.ethereum.request("eth_requestAccounts")
            if accounts:
                wallet_address = accounts[0]
                return wallet_address
        except Exception as e:
            print(f"Error: {e}")
    return None

def interact_with_contract():
    # Crea una instancia del contrato
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    try:
        # Llama a una función en el contrato (por ejemplo, obtener un valor)
        #result = contract.functions.getSomeValue().call()
        #print(f"Cartera: {wallet_address}")
        pass
        #return result
    except Exception as e:
        print(f"Error: {e}")
        return None

# Llamada a la función para interactuar con el contrato
contract_result = interact_with_contract()
if contract_result is not None:
    print(f"Contract Result: {contract_result}")


alchemy_url = "https://eth-sepolia.g.alchemy.com/v2/5APA3WpSw2ESkV84Qlcy-4ZgFQW9I9_M"
w3 = Web3(Web3.HTTPProvider(alchemy_url))

print(w3.is_connected())

#balance = w3.eth.get_balance('0x1c7D08bc2360265296A76b241478AF10ecFb7Fe7')
#print(balance)
