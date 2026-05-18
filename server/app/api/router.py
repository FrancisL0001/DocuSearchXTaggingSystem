from fastapi import APIRouter

from app.api.routes import search, tags

# Single router that combines all route modules.
# Imported and mounted in main.py under the /api/v1 prefix.
api_router = APIRouter()

api_router.include_router(search.router, tags=["search"])
api_router.include_router(tags.router, tags=["tags"])
