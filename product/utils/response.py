
def response(request: any, data: any, status: int, message: str):
    return {
        "message": message,
        "status": status,
        "path": request.path,
        "method": request.method,
        "response": data
    }