from app import app

@app.route('/')
def test():
    return {'message' : "hello, world"}