# Visa Application Service

This repository contains the codebase for the Visa Application Service, a system designed to streamline and manage visa application processes efficiently.

## Folder Structure

The project is organized as follows:

```
visa-application-service/
├── app/
│   ├── init.py               # Package initialization
│   ├── main.py               # FastAPI application entry point
│   ├── config/               # Service Config
│   │   ├── aws.py
│   │   └── database.py       # Database connection and session management
│   ├── models/               # SQLAlchemy models
│   │   ├── init.py
│   │   └── applications.py          # application models
│   ├── api/                  # API endpoints
│   │   ├── init.py
│   │   └── application/             # application domain API
│   │       ├── init.py
│   │       ├── application_routes.py  # application API routes
│   │       ├── application.service.py # application business logic
│   │       └── application.types.py   # application Pydantic schemas/types
│   ├── helpers/                 # utilities
│   │   ├── init.py
│   │   └── auth.py             # Authentication helper functions
├── alembic/                    # Alembic migration files
├── visa_venv/                  # Virtual environment
├── .env                        # Environment variables
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Getting Started

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd visa-application-service
    ```

2. Install dependencies:
    ```bash
    npm install
    ```

3. Set up environment variables in a `.env` file.

4. Start the application:
    ```bash
    npm start
    ```

## Contributing

Contributions are welcome! Please follow the [contribution guidelines](docs/CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).