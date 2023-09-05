
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

## Comprar HostCoin
Per a poder comprar un servidor, has de tenir la nostra moneda a la teva cartera, però el projecte es troba en fase de
desenvolupament, per tant has d'estar a la testnet de Ethereum per a poder operar. Segueix els passos següents:
1. TODO
2. TODO
3. TODO