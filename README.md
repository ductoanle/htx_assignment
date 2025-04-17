A web application that allows users to upload and transcribe audio files using OpenAI's Whisper model.

## Prerequisites

- Python 3.11 or higher
- Poetry (Python package manager)
- Docker (for containerized deployment)
- FFmpeg (for audio processing)

## Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd htx_assignment
```

2. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Navigate to the backend directory:
```bash
cd backend
```

4. Install dependencies using Poetry:
```bash
poetry install
```

5. Create a `.env` file in the backend directory with your configuration:
```bash
cp deploy/env .env
```

6. Run database migrations:
```bash
poetry run alembic upgrade head
```

## Running Tests

1. Make sure you're in the backend directory:
```bash
cd backend
```

2. Run all tests:
```bash
poetry run pytest
```

## Running the Application Locally

1. Start the development server:
```bash
poetry run uvicorn src.htx_transcriber.main:app --reload
```

The application will be available at `http://localhost:8000`

## Docker Deployment

### Building the Docker Image

1. Make sure you're in the backend directory:
```bash
cd backend
```

2. Build the Docker image:
```bash
docker build -t htx-transcriber .
```

### Running the Docker Container

1. Run the container:
```bash
docker run -p 8000:8000 htx-transcriber
```

The application will be available at `http://localhost:8000`