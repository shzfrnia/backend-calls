# backend-calls

## Docker

### prod mode

```
docker build -t backend_calls_prod . --target prod
```

```
docker run -d --name backend_calls_prod -p 80:80 -v ./app:/code/app backend_calls_prod
```

### dev mode

```
docker build -t backend_calls_dev . --target dev
```

```
docker run -d --name backend_calls_dev -p 80:80 -v ./app:/code/app backend_calls_dev
```

## Local runtime

### Create venv

```
python3 -m venv venv
```

### Activate venv

```
source venv/bin/activate
```

### Deactivate venv

```
deactivate
```

### Install requirements

```
pip install --no-cache-dir --upgrade -r requirements.txt
```

## Run dev server

```
fastapi dev app/main.py --port 80 --host 0.0.0.0
```
