from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
load_dotenv()
from app.routes.user_routes import router as user_router


app = FastAPI()

app.include_router(user_router, prefix="/api/users", tags=["users"])

if __name__=="__main__":
    uvicorn.run(app, port=8080)


