from financetracker import create_app
from flask_migrate import migrate, Migrate

app = create_app()



if __name__ == '__main__':
    app.run(debug=True)


