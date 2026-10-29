# Єдина точка запуску, використовує blueprint з пакета app.
from app import app

if __name__ == '__main__':
    app.run(debug=True)
