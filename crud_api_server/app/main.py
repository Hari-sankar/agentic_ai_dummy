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
mcp = FastMCP.from_fastapi(app)

# Create the ASGI app
mcp_app = mcp.http_app(path='/mcp')

# Set the lifespan context for the FastAPI app to use the MCP app's lifespan
app.router.lifespan_context = mcp_app.router.lifespan_context

# mount the MCP server
app.mount("/mcp-server", mcp_app)

print(app.routes)