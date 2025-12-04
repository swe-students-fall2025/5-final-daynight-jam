# Web Application Subsystem

Flask-based web application for the Recipe Jam food recommendation system.

## Quick Start

1. Install dependencies:
```bash
   pip install -r requirements.txt
```

2. Set up environment:
```bash
   cp .env.example .env
   # Edit .env with your MongoDB URI
```

3. Run the application:
```bash
   python -m app.main
```

4. Access at `http://localhost:8000`

## Features

- User authentication (register/login)
- Ingredient management
- Recipe matching based on available ingredients
- Step-by-step cooking instructions