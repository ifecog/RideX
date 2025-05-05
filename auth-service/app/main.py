from fastapi import FastAPI
from app import routes as UserRoute


app = FastAPI()

app.include_router(UserRoute.router, prefix='/api/v1/auth', tags=['users'])


@app.get('/health')
def health_check():
    return {'status': 'Auth Service is up'}