from flask import Flask, redirect

app = Flask(__name__, static_url_path='/static')

# Homepage
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Redirect to Firefox container (port 3001)
@app.route('/proxy')
def proxy():
    return redirect("http://localhost:3001")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
