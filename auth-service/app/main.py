from fastapi import FastAPI
from app.routes import auth_profile as UserRoute


app = FastAPI()

app.include_router(UserRoute.router, prefix='/api/v1/auth', tags=['auth'])


@app.get('/health')
def health_check():
    return {'status': 'Auth Service is up'}