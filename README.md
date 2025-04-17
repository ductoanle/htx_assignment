A web application that allows users to upload and transcribe audio files using OpenAI's Whisper model.

# Potential Improvements

1. **Asynchronous Transcription Processing**
   - Current synchronous API may timeout for large audio files
   - Implement job queue system (e.g., Celery, Redis Queue)
   - Backend returns job ID immediately, allowing frontend to poll status
   - Alternative: Implement long polling in frontend for synchronous API
   - Benefits: Better user experience, more reliable processing, scalable architecture

2. **Enhanced Versioning Support**
   - Do not generate new version for duplicated files
   - Add version comparison features
   - Track version history and changes
   - Support version rollback capabilities
   - Benefits: Better file management, improved user control

3. **Optimized Search Performance**
   - Current LIKE queries may become slow with large datasets
   - Implement PostgreSQL's pg_trgm extension for efficient text search
   - Consider full-text search capabilities
   - Benefits: Improved search performance, better scalability

4. **Object Storage Integration**
   - Move audio file storage to cloud object storage (e.g., Amazon S3)
   - Implement secure file upload/download
   - Add file lifecycle management
   - Benefits: Scalable storage, cost-effective, better security

# Issues to Fix

- Should search only on the original file names which do contain versions.
- More user friendly error messages.

# Backend

## Design Choices

The backend is built with modern Python technologies, each chosen for specific benefits:

- **FastAPI**: A modern, fast web framework for building APIs with Python.

- **SQLAlchemy**: An SQL toolkit and Object-Relational Mapping (ORM) library for Python. It provides a flexible and powerful way to interact with databases while maintaining type safety and database independence.

- **Alembic**: A database migration tool for SQLAlchemy. It enables version control of database schemas, making it easy to track and apply database changes across different environments.

- **Poetry**: A dependency management and packaging tool for Python. It provides deterministic dependency resolution, virtual environment management, and simplified package publishing.

These technologies work together to create a robust, maintainable, and scalable backend system.

## Prerequisites

- Python 3.11 or higher
- Poetry (Python package manager)
- Docker (for containerized deployment)
- FFmpeg (for audio processing)
  - **macOS**: Install using Homebrew
    ```bash
    brew install ffmpeg
    ```
  - **Windows**: 
    1. Download from [FFmpeg official website](https://ffmpeg.org/download.html)
    2. Extract the downloaded archive
    3. Add the `bin` folder to your system's PATH environment variable
    4. Verify installation by running `ffmpeg -version` in a new terminal

## Local Development Setup
Note: Tested in Mac only as I have no Windows machine.

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

# Frontend

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## Docker Deployment

### Building the Docker Image

1. Make sure you're in the frontend directory:
```bash
cd frontend
```

2. Build the Docker image:
```bash
docker build -t htx-transcriber-frontend .
```

### Running the Docker Container

1. Run the container:
```bash
docker run -p 3000:3000 htx-transcriber-frontend
```