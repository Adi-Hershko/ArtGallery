import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.application:app", port=8000, reload=True) # When deploying, change reload to False
