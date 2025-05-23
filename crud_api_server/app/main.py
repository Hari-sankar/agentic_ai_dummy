from fastapi import FastAPI
from .database import Base, engine
from .routers import domains, subdomains, skills, job_titles
from fastapi_mcp import FastApiMCP



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CRUD API Server",
    description="API server for managing domains, subdomains, skills, and job titles.",
    version="1.0.0",
)

app.include_router(domains.router)
app.include_router(subdomains.router)
app.include_router(skills.router)
app.include_router(job_titles.router)

mcp = FastApiMCP(app)

# Mount the MCP server directly to your app
mcp.mount()
@app.get("/")
# Create an MCP server based on this app


def read_root():
    return {"message": "Welcome to the CRUD API Server!"}