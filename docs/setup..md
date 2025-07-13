# Local Development Setup

### Prerequisites

- [Python](https:/python.org/) (v3.13.5+)
- [Docker](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/)
- (Optional) [Postman](https://www.postman.com/) for API testing

### Clone the Repository

```bash
    git clone https://github.com/DSB2004/assignment-api.git
    cd assignment-api
```

### Start Postgres with Docker

```bash
    docker run --name assignment_db \
        -e POSTGRES_USER=postgres \
        -e POSTGRES_PASSWORD=12345678 \
        -e POSTGRES_DB=ez_assignment \
        -p 5432:5432 \
        -d postgres
```

### Start Redis with Docker

```bash
   docker run --name redis_instance \
        -p 6062:6379 \
        -d redis

```

### Setting Up Environment

- Create a .env file in the root of the project.
- Use the .env.example file provided in the repository as a reference.

```bash
    # .env
    DATABASE_URL=postgres://postgres:12345678@localhost:5432/ez_assignment
    REDIS_URL = redis://localhost:6379/0
    JWT_SECRET= <super secure key>


    CLOUD_PUBLIC_KEY= <your image kit public key>
    CLOUD_PRIVATE_KEY= <your image kit private key>
    CLOUD_URL= <your image kit url>

```

- Create a virtual env within project directory

```bash
    # Windows
    python -m venv env
    env\Scripts\activate

    # macOS/Linux
    python3 -m venv env
    source env/bin/activate
```

### Running Server Locally

- Install dependencies:

```bash
    pip install -r requirements.txt
```

- Create Migration Files:

```bash
    python manage.py makemigrations
```

- Make Migrations:

```bash
    python manage.py migrate
```

- Run Celery:

```bash
    # for development on windows
    celery -A config worker --loglevel=info --pool=solo 

    # for development using WSL/Linux/Macos
    celery -A config worker --loglevel=info --concurrency=4
```

- Run Server:

```bash
    python manage.py runserver
```
