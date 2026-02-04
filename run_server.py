#!/usr/bin/env python3
"""
Run FastStore API Server
"""

if __name__ == "__main__":
    import uvicorn
    
    print("Starting FastStore API Server...")
    print("Server will run on: http://127.0.0.1:8080")
    print("Swagger UI: http://127.0.0.1:8080/docs")
    print("ReDoc: http://127.0.0.1:8080/redoc")
    print("Press CTRL+C to stop")
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8080,
        reload=True
    )