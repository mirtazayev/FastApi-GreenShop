import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database.database_config import Base, engine
from routers import auth_router, flowers_router

app = FastAPI()

# origins = {
#     "http://localhost",
#     "http://localhost:3000",
# }

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.include_router(flowers_router.router)
app.include_router(auth_router.router)
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)
