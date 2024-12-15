from app import create_app
from pathlib import Path

# app = create_app()
app = create_app((Path(__file__).parent.joinpath("tests/config.py")))

if __name__ == '__main__':
    app.run(debug=True)
