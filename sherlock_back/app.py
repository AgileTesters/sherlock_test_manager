"""Server runner instance."""
from sherlock_back.api import app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
