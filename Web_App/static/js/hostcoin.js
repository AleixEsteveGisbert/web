//contractAddress = '0x9bd113f79D9bCdc27E06bDc5a08A27c274512Ee8'; // SmartContract TokenExchange1
//contractAddress = '0x7Bd57f1a0f45Eb5C005C07Ef09820D92a2299de4';
//contractAddress = '0xd9145CCE52D386f254917e481eB44e9943F39138'; // 4
//contractAddress = '0xd8b934580fcE35a11B58C6D73aDeE468a2833fa8'; // 5
contractAddress = "0x0Ff0705efe9fb8A300047A365f39BEFfA86D7c6f"; // NOSEKIN IA
var walletAddress;

//Actualitza tots els valors
async function getWalletAddress() {
    // Comprueba si Metamask está instalado
    if (typeof window.ethereum !== 'undefined') {
        // Sol·licita al usuario l'acceso a la seva cartera
        await window.ethereum.request({method: 'eth_requestAccounts'});
        // Obté la instància de web3
        const web3 = new Web3(window.ethereum);
        // Obté la direcció de la cartera actual
        const accounts = await web3.eth.getAccounts();
        walletAddress = accounts[0];
        // Mostra la direcció en la pàgina
        if (document.getElementById('walletAddress') != null) {
            document.getElementById('walletAddress').textContent = `${walletAddress}`;
        }

        getBalances(walletAddress);
    } else {
        // Metamask no està instal·lat
        alert('Per favor, instal·la Metamask per utilizar aquesta funció.');
    }
}

//Agafa el valor the ETH i HostCoins, es crida des de getWalletAdress()
function getBalances(walletAddress) {
    console.log("Funcio getBalances");
    console.log(window.location.pathname);

    const web3 = new Web3(window.ethereum);
    const tokenExchangeContract = new web3.eth.Contract(contractAbi, contractAddress);

    tokenExchangeContract.methods.balances(walletAddress).call((error, balance) => {
        if (error) {
            console.error(error);
        } else {
            console.log(`El saldo de HostCoin a la cartera ${walletAddress} es: ${balance}`);
            // HOC top bar
            document.getElementById('HOCbalance').textContent = `${balance} HOC`;
            // HOC wallet
            if (document.getElementById('HOCbalanceW') != null) {
                document.getElementById('HOCbalanceW').textContent = `${balance} HOC`;
            }
            // HOC new server
            alert(balance);
            if (document.getElementById('HOCbalanceNS') != null) {
                document.getElementById('HOCbalanceNS').textContent = "El balanç d'aquesta cartera és de: " + `${balance} HOC`;
            }
        }
    });

    web3.eth.getBalance(walletAddress)
        .then(balance => {
            const ethBalance = web3.utils.fromWei(balance, 'ether');
            console.log(`El saldo de Ethereum a la cartera ${walletAddress} es: ${ethBalance} ETH`);
            if (document.getElementById('ETHbalance') != null) {
                document.getElementById('ETHbalance').textContent = `${ethBalance} ETH`;
            }

        })
        .catch(error => {
            console.error(error);
        });

}

// Comprar HostCoin
// 0.0001 ether = 1 hostcoin = 0.17~ centims d'euro
async function buyTokens(amount) {
    try {
        await window.ethereum.request({method: 'eth_requestAccounts'});

        const web3 = new Web3(window.ethereum);
        const accounts = await web3.eth.getAccounts();
        const userAccount = accounts[0];
        const tokenExchangeContract = new web3.eth.Contract(contractAbi, contractAddress);

        const tokenPrice = await tokenExchangeContract.methods.tokenPrice().call();
        const totalCost = tokenPrice * amount;

        await tokenExchangeContract.methods.buyTokens(amount).send({
            from: userAccount,
            value: totalCost.toString()
        });

        //Això s'executa quan s'ha completat la transacció
        console.log('Tokens comprats exitosament');
        // accions adicionals

    } catch (error) {
        console.error('Error al comprar tokens:', error);
    }
}

async function spendHostCoins(amount) {
    try {
        // Solicitar permis al usuario per a accedir al seu compte de Ethereum
        await window.ethereum.request({method: 'eth_requestAccounts'});

        // Obtenir el compte de l'usuari actual
        const web3 = new Web3(window.ethereum);
        const tokenExchangeContract = new web3.eth.Contract(contractAbi, contractAddress);
        const accounts = await web3.eth.getAccounts();
        const userAccount = accounts[0];

        // Cridar a la funció spendTokens del contracte HostCoinSale per gastar HostCoin
        await tokenExchangeContract.methods.spendTokens(amount).send({from: userAccount});

        console.log(`S'han gastat ${amount} HostCoin`);

    } catch (error) {
        console.error('Error al gastar HostCoin:', error);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    getWalletAddress(); // Cridar a la funció quan la pàgina carrega al complet
});

//New server
$(document).ready(function () {
    if (window.location.pathname == "/server/new") {
        console.log("New server");
        calcularPreu();
        //alert("total = " + walletHOC);
    }

    //Calcular preu
    function calcularPreu() {
        const cores = parseInt($('#id_cores').val());
        const ram = parseInt($('#id_ram').val());
        let hocCoresPrice = cores * 1;
        let hocRamPrice = ram * 1;
        let total = hocCoresPrice + hocRamPrice;
        document.getElementById('HOCprice').textContent = "El preu diari d'aquest servidor serà de: " + total + " HOC";

        alert("cores = " + hocCoresPrice + " | ram = " + hocRamPrice + " | Total en HOC: " + total + " | Total: ");
    }

    $('#id_cores, #id_ram').change(function () {
        calcularPreu();
    })

})

contractAbi = [
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
        "anonymous": false,
        "inputs": [
            {
                "indexed": false,
                "internalType": "address",
                "name": "buyer",
                "type": "address"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "TokensPurchased",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": false,
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": false,
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