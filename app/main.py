from fastapi import FastAPI

from .routers import rooms

app = FastAPI()


app.include_router(prefix='/api', router=rooms.router)


@app.get("/")
def root():
    return {"Hello": "app"}
