from SIG_EmDis import app, db

@app.route('/')
@app.route('/login')
def login():
    return '<h1>Haloo ini Login </h1>'