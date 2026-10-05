# Library Management System
A modular terminal-based Library Management System built with Python.

The project was designed to apply professional software engineering concepts including:

- Object-Oriented Programming
- Layered Architecture
- Repository Pattern
- Service Layer
- Authentication & Authorization
- Session Management
- JSON Persistence
- Logging
- Exception Handling
- Automated Testing
- Clean separation of concerns

## Features

### Authentication

- User registration
- User login/logout
- Password hashing
- Session management
- Role-based authorization
- Account activation/deactivation
- Password changing

### Books

- Add books
- List books
- Search by title
- Search by author
- Search by classification
- Find book by ID
- Update book information
- Delete books
- Track book availability

### Borrowing

- Borrow books
- Return books
- Borrowing limits
- Borrowing duration
- Active borrowing tracking
- Borrowing history
- Late-return fines

### Members

- List members
- Search members
- View member details
- View member borrowing history
- Activate/deactivate members

### Reports

- Library statistics
- Active/returned/overdue borrowings
- Fine statistics
- Most borrowed books
- Most active users

### Technical Features

- Generic JSON storage
- Atomic file writes
- Data validation
- Custom exceptions
- Application logging
- Automated unit/service tests

## Architecture
The application follows a layered architecture:

```
                UI
                 │
                 ▼
             Services
                 │
                 ▼
           Repositories
                 │
                 ▼
              Storage
                 │
                 ▼
           JSON Files
```

### UI Layer
Responsible only for:

- Displaying screens
- Reading user input
- Calling services
- Showing results/errors
UI must not contain business logic or direct JSON access.

### Service Layer
Responsible for:

- Business rules
- Validation
- Authorization
- Application workflows
- Coordination between repositories

### Repository Layer
Responsible for:

- Loading entities
- Saving entities
- Abstracting persistence

### Storage Layer
Responsible only for:

- Reading/writing JSON
- File handling
- Atomic writes
- Storage-level errors

## Project Structure

```
LibraryManagmentWithPython/
│
├── main.py
│
├── Models/
│   ├── book.py
│   ├── user.py
│   └── borrowing.py
│
├── repositories/
│   ├── book_repository.py
│   ├── user_repository.py
│   └── borrowing_repository.py
│
├── Services/
│   ├── book_service.py
│   ├── user_service.py
│   ├── auth_service.py
│   ├── borrowing_service.py
│   ├── report_service.py
│   └── member_service.py
│
├── Storage/
│   └── json_storage.py
│
├── auth/
│   ├── session.py
│   ├── password_hasher.py
│   └── exceptions.py
│
├── UI/
│   ├── auth/
│   ├── books/
│   ├── borrowing/
│   ├── members/
│   ├── menus/
│   ├── profile/
│   └── reports/
│
├── config/
│   └── config.py
│
├── data/
│   ├── books.json
│   ├── users.json
│   └── borrowings.json
│
├── logs/
│   └── library.log
│
├── tests/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Running the Project
Create and activate a virtual environment:

```
python -m venv .venv
```
Windows:

```
.venv\Scripts\activate
```
Install dependencies:

```
pip install -r requirements.txt
```
Run the application:

```
python main.py
```

## Running Tests
Run the complete test suite:

```
python -m pytest -q
```
Current test status:

```
55 passed
```

## Design Principles
The project follows several important principles:

### Separation of Concerns
Each layer has one clear responsibility.

### Single Source of Truth
Borrowing information is stored in the borrowing system rather than duplicating borrowing state inside the user model.

### Dependency Direction
Higher-level application logic depends on abstractions such as repositories instead of directly manipulating JSON files.

### Explicit Business Rules
Rules such as:

- maximum active borrowings
- book availability
- duplicate books
- overdue fines
- librarian permissions
are enforced in the service layer.

### Persistence Safety
JSON writes use atomic replacement to reduce the risk of corrupted data.

## Future Improvements
Possible future versions include:

- SQLite database
- Database migrations
- REST API
- Web interface
- Advanced analytics
- Recommendation system
- Machine learning integration

## Learning Goal
This project was built as a practical transition from Python fundamentals toward professional software engineering and Artificial Intelligence.

The next major learning phase is focused on:

```
NumPy
   ↓
Pandas
   ↓
Matplotlib
   ↓
Mathematics for ML
   ↓
Scikit-learn
   ↓
Machine Learning
   ↓
Deep Learning
   ↓
Artificial Intelligence
```
