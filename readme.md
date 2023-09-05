
<div align="center" style="margin-top: 20px">
  <img src="https://github.com/aleixBY23/web/blob/main/Web_App/static/logo/logo_400x100.png?raw=true" alt="GameSave">
</div>

Aquest projecte tracta sobre el procés de desenvolupament d’una plataforma web on l’usuari pot comprar servidors per a videojocs que es despleguen automàticament, integrant la nostra pròpia criptomoneda i on l’usuari paga solament pels recursos que necessita.

## Requisits

- Python (versió 3.10)
- Django (versió 4.2)
- Altres dependències (veure `requirements.txt`)
- Has de tenir instal·lat docker al teu ordinador [Docker Desktop](https://docs.docker.com/get-docker/)
- La extensió de [MetaMask](https://metamask.io/download/) instal·lada en el teu navegador
- 
## Instalació

1. Clona el repositori:
   ```bash
   git clone https://github.com/aleixBY23/web

2. Ves fins el directori del projecte
   ```bash
   cd web
   
3. Instal·la les dependències
   ```bash
   pip install -r requirements.txt
   
4. Si es necessari, aplica les migracions a la base de dades:
   ```bash
   python manage.py migrate
   
5. Ja pots iniciar el servidor web:
   ```bash
   python manage.py runserver

Pots veure la web a  `http://localhost:8000/`.

## Configuració
Per a poder comprar un servidor, has de tenir la nostra moneda a la teva cartera, però el projecte es troba en fase de
desenvolupament, per tant has d'estar a la testnet de Ethereum per a poder operar. Segueix els passos següents:

1. Registrar-se a [Alchemy.com](https://dashboard.alchemy.com/)
2. Una volta registrat, hem de crear una App anant a `Apps` > `Create new app`
3. Emplenar els camps amb les dades següents 
   - `Chain`: Ethereum 
   - `Network`: Ethereum Sepolia
   - `Name`: El que vulguis
   - `Description`: El que vulguis
4. Una volta creada, entrar a l'app i clicar a `ADD TO WALLET` en la part superior dreta. S'obrirà una finestra de Metamask on haurem de clicar `Approve` > `Approve` > `Switch network`.
5. Per a aconseguir Ethereums per a poder fer proves, introduïr la nostra direcció de cartera (la qual pots trobar clicant a MetaMask i a la part superior) a [sepoliafaucet](https://sepoliafaucet.com/) on podem rebre 0.5 ETH diaris.
6. Accedir a la nostra web on MetaMask demanarà accés. Tria la teva cartera, clica `Next` > `Connect`.
7. Ja pots començar a operar amb el nostre token dins la nostra plataforma.
