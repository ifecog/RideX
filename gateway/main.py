from fastapi import FastAPI
import httpx

app = FastAPI()


@app.get('/health')
def health():
    return {"status": "Gateway is running"}


@app.get('/auth-health')
async def auth_health():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://auth-service:8000/health")
            return {"auth_service_response": response.json()}
        except Exception as e:
            return {"error": str(e)}
        
        