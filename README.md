# Digital Quiz App Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [File Structure](#file-structure)
6. [Technical Details](#technical-details)
7. [Testing](#testing)
8. [Building Executable](#building-executable)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)

## Project Overview

The Digital Quiz App is a comprehensive desktop application built with Python and CustomTkinter that provides a complete quiz management system. The application supports user authentication, question authoring, quiz taking, and performance tracking.

### Key Technologies
- **Python 3.x** - Core programming language
- **CustomTkinter** - Modern GUI framework
- **SQLite** - Database for user data and questions
- **PyInstaller** - Executable creation
- **Unittest** - Testing framework

## Features

### User Management
- Secure user registration and authentication
- Password hashing with salt for security
- Guest access option
- User-specific quiz history

### Question Management
- Support for multiple question types:
  - Multiple Choice Questions (MCQ)
  - True/False Questions
  - Fill-in-the-blank Questions
- Question authoring interface
- Import questions from CSV/JSON files
- Database storage for questions

### Quiz Functionality
- Customizable quiz duration (60s to 600s)
- Progress tracking with visual progress bar
- Timer with color-coded warnings
- Navigation between questions
- Answer review before submission
- Automatic submission on time expiry

### Results and History
- Detailed quiz results with question-by-question breakdown
- Performance statistics and scoring
- User history with date tracking
- Percentage calculations and performance messages

### User Interface
- Modern gradient background design
- Responsive layout
- Intuitive navigation
- Error handling with user-friendly messages

## Installation

### Prerequisites
```bash
Python 3.x
pip (Python package manager)
```

### Required Dependencies
```bash
pip install customtkinter
pip install sqlite3  # Usually included with Python
pip install pathlib   # Usually included with Python
```

### Setup
1. Clone the repository:
```bash
git clone https://github.com/Ajayikx/Group-13-Digital-Quiz-App-python-advance-cohort-28-.git
```

2. Navigate to the project directory:
```bash
cd Group-13-Digital-Quiz-App-python-advance-cohort-28-/DigitalQuizApp
```

3. Run the application:
```bash
python app.py
```

## Usage

### First Time Setup
1. Launch the application
2. Register a new user account or continue as guest
3. Create questions using the "Create Questions" feature
4. Take your first quiz

### Creating Questions
1. Click "Create Questions" from the main menu
2. Select question type (MCQ, True/False, or Fill-in)
3. Enter question text and options
4. Specify the correct answer
5. Click "Add Question" to save

### Taking a Quiz
1. Select quiz duration from the settings
2. Click "Take Quiz"
3. Navigate through questions using Previous/Next buttons
4. Use "Review Answers" to check your responses
5. Submit when ready or when time expires

### Importing Questions
1. Prepare CSV or JSON file with questions
2. Click "Import Quiz File"
3. Select your file
4. Questions will be added to the database

#### CSV Format Example:
```csv
question,type,options,answer
"What is 2+2?",mcq,"2|3|4|5",4
"Python is interpreted",truefalse,"",True
"Capital of France",fill,"",Paris
```

#### JSON Format Example:
```json
[
  {
    "question": "What is 2+2?",
    "type": "mcq",
    "options": ["2", "3", "4", "5"],
    "answer": "4"
  }
]
```

## File Structure

```
DigitalQuizApp/
├── app.py                                  # Main application file
├── test_app.py                             # Test suite (if in same directory)
├── users.db                                # User database (created automatically)
├── quiz.db                                 # Questions and history database
├── questions.csv                           # Sample questions file
├── questions.json                          # Sample questions file
├── Project_Research_Proposal.txt/          # Proposal files (before building)
├── pipfile                                 # for installing dependancies
├── pipfile.lock                            # for installing dependancies
└── README.txt                              # Basic readme file

tests/
└── test_app.py                             # External test suite
```

## Technical Details

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    salt BLOB NOT NULL,
    password_hash BLOB NOT NULL
)
```

#### Questions Table
```sql
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    text TEXT NOT NULL,
    choices TEXT,
    answer TEXT NOT NULL
)
```

#### History Table
```sql
CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Data Storage
- **Development**: Data stored in application directory
- **Executable**: Data stored in `%APPDATA%\Local\QuizApp\` for persistence

### Security Features
- Password hashing using PBKDF2 with SHA-256
- 16-byte random salt generation
- 100,000 iterations for key derivation
- Secure password comparison using `secrets.compare_digest`

### Question Types Implementation
- **MCQ**: Radio button selection with lettered options (A, B, C, D)
- **True/False**: Binary radio button selection
- **Fill-in**: Text entry with case-insensitive matching

## Testing

The application includes a comprehensive test suite covering:

### Test Categories
- Database operations
- User authentication
- Question management
- Quiz logic
- Data persistence
- Input validation
- Error handling

### Running Tests
```bash
# From the tests directory or wherever test_app.py is located
python test_app.py
```

### Test Coverage
- Unit tests for all major functions
- Integration tests for complete workflows
- Performance tests for database operations
- Security tests for authentication

## Building Executable

### Using PyInstaller
```bash
# Install PyInstaller
pip install pyinstaller

# Navigate to app directory
cd DigitalQuizApp

# Create executable
pyinstaller --onefile --windowed --name="DigitalQuizApp" app.py
```

### Build Options
```bash
# With custom icon
pyinstaller --onefile --windowed --icon=icon.ico --name="DigitalQuizApp" app.py

# For debugging (shows console)
pyinstaller --onefile --console --name="DigitalQuizApp_Debug" app.py
```

### Distribution
- Executable will be created in `dist/` folder
- File size: ~50-100MB (includes Python interpreter)
- Works on Windows machines without Python installed

## Troubleshooting

### Common Issues

#### "No questions available"
- **Cause**: Database is empty
- **Solution**: Create questions or import from file

#### "Database Error"
- **Cause**: Insufficient permissions or corrupted database
- **Solution**: Check file permissions, delete database files to reset

#### "Import failed"
- **Cause**: Incorrect file format
- **Solution**: Verify CSV/JSON format matches examples

#### Timer not working in executable
- **Cause**: Threading issues in PyInstaller
- **Solution**: Already handled in current implementation

#### Data not persisting in executable
- **Cause**: Temporary directory usage
- **Solution**: Already fixed - data stored in AppData

### Performance Optimization
- Database indexed on username for faster queries
- Lazy loading of questions
- Efficient memory management for large question sets

### Debugging
```bash
# Enable debug mode
python app.py --debug

# Check database contents
sqlite3 quiz.db
.tables
SELECT * FROM questions;
```

## Contributing
1.Igbalaye Faizal
2.Ajayi Abdulquadri
3.Fayomi Oluwapelumi
4.Chizea Uchechuku Daniel
5.Ugwu Chinanu Nestor

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make changes with appropriate tests
4. Run the test suite
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings for functions
- Include error handling

### Adding Features
1. Update the main application (`app.py`)
2. Add corresponding tests in test suite
3. Update documentation
4. Test executable creation

## API Reference

### Main Classes

#### `QuizWindow`
Main application window with navigation between screens.

**Methods:**
- `show_login()` - Display login screen
- `show_register()` - Display registration screen
- `show_home()` - Display main menu
- `show_quiz()` - Start quiz session
- `show_author()` - Open question authoring
- `show_history()` - Display user history

#### `QuizScreen`
Handles quiz functionality and user interaction.

**Methods:**
- `_load_question()` - Display current question
- `_next_question()` - Navigate to next question
- `_prev_question()` - Navigate to previous question
- `_submit_quiz()` - Process quiz submission
- `_show_results()` - Display quiz results

#### `AuthorScreen`
Question creation and editing interface.

**Methods:**
- `_add_question()` - Save new question to database
- `_clear_fields()` - Reset form inputs

### Database Functions

#### User Management
- `register_user(username, password)` - Create new user account
- `authenticate_user(username, password)` - Verify user credentials

#### Question Management
- `insert_question(question, options, answer, qtype)` - Add question to database
- `load_questions_from_db()` - Retrieve all questions

#### History Management
- `save_history(username, score, total)` - Record quiz results
- `load_history(username)` - Get user's quiz history

## Version History

### Version 1.0.0
- Initial release
- Basic quiz functionality
- User authentication
- Question authoring
- CSV/JSON import
- Executable support
- Comprehensive test suite

## License

This project is part of an educational assignment for Python Advanced Cohort 28.

## Support

For issues and questions, please refer to the repository's issue tracker or contact the development team.

---

**Project Repository:** [Group-13-Digital-Quiz-App-python-advance-cohort-28-](https://github.com/Ajayikx/Group-13-Digital-Quiz-App-python-advance-cohort-28-)

**Last Updated:** September 2025
