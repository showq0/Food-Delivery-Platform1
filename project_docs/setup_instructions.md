## Prerequisites

- Python 3.8+
- `pip` installed

## Installation

1. Clone the repository:

```bash
gh repo clone showq0/Food-Delivery-Platform1
cd Food-Delivery-Platform1
```

Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```
create a .env file in the root directory
```bash
# Database
SQLALCHEMY_DATABASE_URI=sqlite:///food_platform.sqlite3
SQLALCHEMY_TRACK_MODIFICATIONS=False

# Flask Secret
SECRET_KEY=your_secret_key

# JWT Configuration
JWT_SECRET_KEY=super-secret-key
JWT_TOKEN_LOCATION=cookies
JWT_COOKIE_SECURE=False
JWT_COOKIE_CSRF_PROTECT=False
```
Install all requirements:

```bash
pip install -r requirements.txt
```

### RUN project

```bash
python app.py
```
