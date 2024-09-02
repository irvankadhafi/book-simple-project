# Book Simple Project

This repository contains two main components:

- **book-api**: A FastAPI backend service.
- **book-frontend**: A Vue.js frontend application.

## Book API Architecture Overview

The Book API project is built using the FastAPI framework, which is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. The architecture is designed to be clean, modular, and scalable, making it easier to maintain and extend.

### Key Components

#### 1. **FastAPI**

FastAPI is the core framework used for building the API. It is chosen for its performance, ease of use, and automatic generation of interactive API documentation.

#### 2. **Modular Structure**

The project is structured into various modules to separate concerns and improve maintainability. Each module has a specific responsibility:

- **app/config**: Contains configuration-related files, including environment variables.
- **app/db**: Handles database connections, migrations, and interactions.
- **app/delivery/httpsvc**: Contains the HTTP service layer, including routes and request handlers.
- **app/models**: Defines the data models used throughout the application, typically linked with the database.
- **app/repositories**: Acts as the data access layer, interacting with the models and performing CRUD operations.
- **app/schemas**: Contains Pydantic schemas that define the structure of request and response payloads.
- **app/usecases**: Encapsulates the business logic of the application, ensuring that the application logic is separate from the data access and delivery layers.

#### 3. **Database Management**

The application uses PostgreSQL as the primary database, managed through SQLAlchemy. Redis is also used for caching purposes, providing faster access to frequently requested data.

- **Migrations**: Database migrations are managed through custom scripts in the `app/db/migrations.py` file. Migrations ensure that the database schema remains consistent across different environments.

#### 4. **Dependency Injection**

FastAPI's dependency injection system is leveraged to manage and inject dependencies like database connections, cache managers, and use case instances into route handlers. This makes the application more modular and testable.

#### 5. **Caching**

Caching is implemented using Redis. By caching frequently accessed data, the application can reduce the load on the database and improve response times.

#### 6. **Error Handling**

Custom exceptions are defined in the `app/core/exceptions.py` file, and are used throughout the application to handle errors consistently. These exceptions are caught and formatted into standard API error responses.

#### 7. **Testing**

The project includes unit tests for different components, such as repositories, use cases, and handlers. Tests are located in the `tests` directory and can be run using `pytest`.

### Benefits of the Architecture

1. **Scalability**: The modular structure allows individual components to be scaled independently. For instance, the database or caching layer can be scaled without affecting the business logic or delivery layer.
2. **Maintainability**: With a clear separation of concerns, each module can be maintained, updated, or replaced without affecting other parts of the application. This reduces the risk of introducing bugs when making changes.
3. **Testability**: Dependency injection and modular design make it easier to write unit tests, as components can be isolated and tested independently.
4. **Performance**: FastAPI, combined with Redis caching, ensures high performance. The application can handle a large number of concurrent requests with low latency.
5. **Extensibility**: The architecture supports adding new features or services with minimal changes to the existing codebase. For example, adding a new API endpoint or integrating a new service can be done with minimal impact on the rest of the application.
6. **Maintainability**: With a clear separation of concerns, each module can be maintained, updated, or repla

## Getting Started

To run the project, you'll use Docker Compose to manage both the backend and frontend services.

### Folder Structure

```
book-project/
├── book-api/
│   ├── app/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
├── book-frontend/
│   ├── src/
│   ├── Dockerfile
│   └── README.md
├── docker-compose.yml
└── README.md
```

### Prerequisites

- Docker
- Docker Compose

### Setting Up

1. **Clone the repository**:

   ```bash
   git clone https://github.com/irvankadhafi/book-simple-project.git
   cd book-simple-project
   ```
2. **Run Docker Compose**:

   ```bash
   docker-compose up --build
   ```

   This command will build and start both the `book-api` and `book-frontend` services.

### Populating Books Data

You can quickly populate the database with sample book data using the `populate_books.sh` script located in the `book-api` folder. This script uses the FastAPI endpoints to add several book records.

To run the script:

```bash
cd book-api
bash populate_books.sh
```

This will send multiple POST requests to the API to create book records, with a 1-second interval between each request.

### Example API Usage with cURL

Here are examples of how to use the API endpoints with cURL.

#### Create a Book

```bash
curl -X POST "http://localhost:8000/api/v1/books/" -H "Content-Type: application/json" -d '{
  "title": "New Book Title",
  "author": "Author Name",
  "published_date": "2024-01-01",
  "isbn": "9781234567890",
  "pages": 250
}'
```

#### Get a Book by ID

```bash
curl -X GET "http://localhost:8000/api/v1/books/1"
```

#### Search Books

```bash
curl -X GET "http://localhost:8000/api/v1/books/" -G --data-urlencode "query=PostgreSQL" --data-urlencode "page=1" --data-urlencode "size=10" --data-urlencode "sort=created_at:desc"
```

#### Update a Book

```bash
curl -X PUT "http://localhost:8000/api/v1/books/1" -H "Content-Type: application/json" -d '{
  "title": "Updated Book Title",
  "author": "Updated Author Name",
  "published_date": "2024-02-01",
  "isbn": "9781234567890",
  "pages": 300
}'
```

#### Delete a Book

```bash
curl -X DELETE "http://localhost:8000/api/v1/books/1"
```

### Running Migrations

To manage database migrations:

- **Apply migrations**:

  ```bash
  docker-compose exec book-api python -m app.cli migrate_up
  ```
- **Revert migrations**:

  ```bash
  docker-compose exec book-api python -m app.cli migrate_down
  ```

### Running the Server

To run the server using Docker Compose, use:

```bash
docker-compose up --build
```

Or, to run it manually inside the container:

```bash
docker-compose exec book-api python -m app.cli server
```

### Running Unit Tests

To run the unit tests inside the `book-api` container:

```bash
docker-compose exec book-api pytest tests/unit
```

## API List

### 1. Create a Book

**Endpoint**: `/api/v1/books/`

**Method**: `POST`

**Payload**:

```json
{
  "title": "New Book Title",
  "author": "Author Name",
  "published_date": "2024-01-01",
  "isbn": "9781234567890",
  "pages": 250
}
```

### 2. Get a Book by ID

**Endpoint**: `/api/v1/books/{book_id}`

**Method**: `GET`

### 3. Search Books

**Endpoint**: `/api/v1/books/`

**Method**: `GET`

**Query Parameters**:

- `query`: Search term for title, author, or ISBN.
- `page`: Page number.
- `size`: Number of items per page.
- `sort`: Sort order (e.g., `created_at:desc`).

### 4. Update a Book

**Endpoint**: `/api/v1/books/{book_id}`

**Method**: `PUT`

**Payload**:

```json
{
  "title": "Updated Book Title",
  "author": "Updated Author Name",
  "published_date": "2024-02-01",
  "isbn": "9781234567890",
  "pages": 300
}
```

### 5. Delete a Book

**Endpoint**: `/api/v1/books/{book_id}`

**Method**: `DELETE`
