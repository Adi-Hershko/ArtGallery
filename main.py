import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.app:app", port=8000, reload=True) # When deploying, change reload to False
    # Maybe we should create the DB in here?
    # create_database()