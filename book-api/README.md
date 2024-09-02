
# Book Simple Project

This repository contains two main components:
- **book-api**: A FastAPI backend service.
- **book-frontend**: A Vue.js frontend application.

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
