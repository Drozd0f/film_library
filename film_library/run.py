from src.app import create_app
from src.db.database import init_db


def main():
    app = create_app()
    app.app_context().push()
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
