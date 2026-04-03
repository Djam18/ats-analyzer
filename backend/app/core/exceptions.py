from fastapi import Request
from fastapi.responses import JSONResponse
 
async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=404,
        content={"error": {"code": "NOT_FOUND", "message": "Resource not found"}})
 
async def internal_error_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500,
        content={"error": {"code": "INTERNAL_ERROR", "message": "Internal server error"}})
