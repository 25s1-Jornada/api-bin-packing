# Running the project

First create a venv

```bash

    python -m venv .venv

```

Then activate the .venv

```bash

    source .venv/bin/activate

```
Install requirements.txt

```bash

    pip install -r requirements.txt

```

After setting the environment, let`s setup the DB

```bash

    python populate.py

```

The last step it's just run the main

```bash

    python main.py

```


Run the container

```bash

    docker-compose up --build

```

Teste Funcional de Registros: https://docs.google.com/spreadsheets/d/1xmPjmkWVIUrXNVcmguXJSGu3JWRGIdxMXj_lB2CB_u4/edit?gid=0#gid=0
