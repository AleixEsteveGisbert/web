# GameSave

Descripció

## Requisits

- Python (versió 3.10)
- Django (versió 4.2)
- Altres dependències (veure `requirements.txt`)
- Has de tenir instal·lat docker al teu ordinador [Docker Desktop](https://docs.docker.com/get-docker/)
## Instalació

1. Clona el repositori:
   ```bash
   git clone https://github.com/aleixBY23/web

2. Ves fins el directori del projecte i instal·la les dependències
   ```bash
   pip install -r requirements.txt
   
3. Si es necessari, aplica les migracions a la base de dades:
   ```bash
   python manage.py migrate
   
4. Ja pots iniciar el servidor web:
   ```bash
   python manage.py runserver

Pots veure la web a  `http://localhost:8000/`.