# backend-calls

## prod mode
```
docker build -t backend_calls_prod . --target prod
```
```
docker run -d --name backend_calls_prod -p 80:80 -v ./app:/code/app backend_calls_prod
```

## dev mode
```
docker build -t backend_calls_dev . --target dev
```
```
docker run -d --name backend_calls_dev -p 80:80 -v ./app:/code/app backend_calls_dev
```
