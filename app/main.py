from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.pull_request_api import router as pr_router
from app.api.team_api import router as team_router
from app.api.user_api import router as user_router

app = FastAPI()


app.include_router(team_router, prefix="/team", tags=["Teams"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(pr_router, prefix="/pullRequest", tags=["PullRequests"])


ERROR_STATUS = {
    "NOT_FOUND": 404,
    "TEAM_EXISTS": 409,
    "PR_EXISTS": 409,
    "PR_MERGED": 409,
    "NOT_ASSIGNED": 409,
    "NO_CANDIDATE": 409,
}


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    code = exc.args[0]

    status_code = ERROR_STATUS.get(code, 400)

    if code == "NOT_FOUND":
        message = "resource not found"
    else:
        message = "error"

    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
            }
        },
    )


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
