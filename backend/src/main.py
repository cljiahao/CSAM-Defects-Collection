import uvicorn

# TODO: Create Docker for NGINX (Load Balancing)
# TODO: Gunicorn to have mutliple worker
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8010, reload=True, log_level="info")
