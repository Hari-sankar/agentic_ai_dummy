from fastapi import FastAPI
from .database import Base, engine
from .routers import domains, subdomains, skills, job_titles
from fastmcp import FastMCP



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


@app.get("/")
def read_root():
    return {"message": "Hello from root"}

# Create your FastMCP server as well as any tools, resources, etc.
from starlette.routing import Mount

# Create your FastMCP server as well as any tools, resources, etc.
mcp = FastMCP("MyServer")

# Create the ASGI app
mcp_app = mcp.http_app(path='/mcp')

# Create a FastAPI app and mount the MCP server
app = FastAPI(lifespan=mcp_app.lifespan)
app.mount("/mcp-server", mcp_app)

print(app.routes)