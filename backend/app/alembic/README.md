### generate migration (if change db)

```
alembic revision --autogenerate
```
```
alembic revision --autogenerate -m "Add new models"
```

### update db version

```
alembic upgrade head [version]
```
