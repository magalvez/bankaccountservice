from app import app, auth
from app.api import api

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", threaded=True, port=8300)
