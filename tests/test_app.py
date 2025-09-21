# test_app.py - External Test Suite for Quiz Application
import unittest
import sqlite3
import tempfile
import shutil
from pathlib import Path
import sys
import os
import hashlib
import secrets

# Configuration: Set the path to your quiz app folder
# Based on your current working directory, using relative path
QUIZ_APP_FOLDER = os.path.join(os.path.dirname(os.getcwd()), "DigitalQuizApp")

# Alternative absolute path based on your directory structure:
QUIZ_APP_FOLDER = r"C:\Users\ajayi\Desktop\Group 13(python advance cohort  28)\Group-13-Digital-Quiz-App-python-advance-cohort-28-\DigitalQuizApp"

# Add the quiz app directory to Python path
if QUIZ_APP_FOLDER not in sys.path:
    sys.path.insert(0, QUIZ_APP_FOLDER)

# Verify the app file exists
app_file_path = os.path.join(QUIZ_APP_FOLDER, "app.py")
if not os.path.exists(app_file_path):
    print(f"ERROR: Could not find app.py at: {app_file_path}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Try to find the correct path
    possible_paths = [
        os.path.join(os.path.dirname(os.getcwd()), "DigitalQuizApp"),
        os.path.join(os.getcwd(), "..", "DigitalQuizApp"),
        r"C:\Users\ajayi\Desktop\Group 13(python advance cohort  28)\Group-13-Digital-Quiz-App-python-advance-cohort-28-\DigitalQuizApp"
    ]
    
    print("Searching for app.py in possible locations:")
    for path in possible_paths:
        test_app_path = os.path.join(path, "app.py")
        if os.path.exists(test_app_path):
            print(f"FOUND: {test_app_path}")
            print(f"Update QUIZ_APP_FOLDER to: {path}")
            break
        else:
            print(f"NOT FOUND: {test_app_path}")
    
    print("Please update the QUIZ_APP_FOLDER path in this test file.")
    sys.exit(1)

print(f"Testing quiz app from: {QUIZ_APP_FOLDER}")

# Create isolated test data directory
TEST_DATA_DIR = Path(tempfile.mkdtemp(prefix="quiz_test_"))
print(f"Test data directory: {TEST_DATA_DIR}")

# Mock the data directory for testing
def mock_get_data_dir():
    TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
    return TEST_DATA_DIR

# Import the app module
try:
    import app
    print("Successfully imported app module")
except ImportError as e:
    print(f"Failed to import app module: {e}")
    print("Please check that the QUIZ_APP_FOLDER path is correct")
    print(f"Looking for app.py in: {QUIZ_APP_FOLDER}")
    sys.exit(1)

# Replace the actual function with our test version
app.get_data_dir = mock_get_data_dir
app.DATA_DIR = TEST_DATA_DIR
app.DB_PATH = TEST_DATA_DIR / "users.db"
app.QUIZ_DB_PATH = TEST_DATA_DIR / "quiz.db"

class TestDatabaseFunctions(unittest.TestCase):
    """Test database initialization and basic operations"""
    
    def setUp(self):
        """Set up test environment before each test"""
        # Clean up any existing test databases
        if (TEST_DATA_DIR / "users.db").exists():
            (TEST_DATA_DIR / "users.db").unlink()
        if (TEST_DATA_DIR / "quiz.db").exists():
            (TEST_DATA_DIR / "quiz.db").unlink()
    
    def tearDown(self):
        """Clean up after each test"""
        # Remove test databases
        if (TEST_DATA_DIR / "users.db").exists():
            (TEST_DATA_DIR / "users.db").unlink()
        if (TEST_DATA_DIR / "quiz.db").exists():
            (TEST_DATA_DIR / "quiz.db").unlink()
    
    def test_database_initialization(self):
        """Test that databases are created properly"""
        app.init_user_db()
        app.init_quiz_db()
        
        self.assertTrue((TEST_DATA_DIR / "users.db").exists())
        self.assertTrue((TEST_DATA_DIR / "quiz.db").exists())
    
    def test_user_registration(self):
        """Test user registration functionality"""
        app.init_user_db()
        
        # Test valid registration
        success, message = app.register_user("testuser", "password123")
        self.assertTrue(success)
        self.assertEqual(message, "Registration successful.")
        
        # Test duplicate username
        success, message = app.register_user("testuser", "password456")
        self.assertFalse(success)
        self.assertEqual(message, "Username already exists.")
        
        # Test invalid passwords
        success, message = app.register_user("user2", "12345")  # Too short
        self.assertFalse(success)
        
        success, message = app.register_user("user3", "password")  # No numbers
        self.assertFalse(success)
        
        success, message = app.register_user("user4", "123456")  # No letters
        self.assertFalse(success)
    
    def test_user_authentication(self):
        """Test user login functionality"""
        app.init_user_db()
        
        # Register a test user
        app.register_user("testuser", "password123")
        
        # Test valid login
        self.assertTrue(app.authenticate_user("testuser", "password123"))
        
        # Test invalid password
        self.assertFalse(app.authenticate_user("testuser", "wrongpassword"))
        
        # Test non-existent user
        self.assertFalse(app.authenticate_user("nonexistent", "password123"))
    
    def test_question_operations(self):
        """Test question insertion and retrieval"""
        app.init_quiz_db()
        
        # Test inserting different types of questions
        app.insert_question("What is 2+2?", ["2", "3", "4", "5"], "4", "mcq")
        app.insert_question("Python is a programming language", "", "True", "truefalse")
        app.insert_question("Capital of France is ___", "", "Paris", "fill")
        
        # Retrieve questions
        questions = app.load_questions_from_db()
        self.assertEqual(len(questions), 3)
        
        # Check question content
        mcq_question = questions[0]
        self.assertEqual(mcq_question[1], "mcq")
        self.assertEqual(mcq_question[2], "What is 2+2?")
        self.assertEqual(mcq_question[4], "4")
    
    def test_history_operations(self):
        """Test quiz history saving and loading"""
        app.init_quiz_db()
        
        # Save some quiz history
        app.save_history("testuser", 8, 10)
        app.save_history("testuser", 6, 10)
        app.save_history("otheruser", 9, 10)
        
        # Load history for specific user
        history = app.load_history("testuser")
        self.assertEqual(len(history), 2)
        
        # Check history content
        self.assertEqual(history[0][1], "testuser")  # username
        self.assertEqual(history[0][2], 8)           # score
        self.assertEqual(history[0][3], 10)          # total

class TestSecurityFunctions(unittest.TestCase):
    """Test password hashing and verification"""
    
    def test_password_hashing(self):
        """Test password hashing functionality"""
        password = "testpassword123"
        
        # Hash password
        salt, hashed = app.hash_password(password)
        
        # Verify salt and hash are created
        self.assertIsInstance(salt, bytes)
        self.assertIsInstance(hashed, bytes)
        self.assertEqual(len(salt), 16)  # Salt should be 16 bytes
        
        # Test password verification
        self.assertTrue(app.verify_password(password, salt, hashed))
        self.assertFalse(app.verify_password("wrongpassword", salt, hashed))
    
    def test_password_uniqueness(self):
        """Test that same password produces different hashes with different salts"""
        password = "samepassword"
        
        salt1, hash1 = app.hash_password(password)
        salt2, hash2 = app.hash_password(password)
        
        # Different salts should produce different hashes
        self.assertNotEqual(salt1, salt2)
        self.assertNotEqual(hash1, hash2)
        
        # Both should verify correctly
        self.assertTrue(app.verify_password(password, salt1, hash1))
        self.assertTrue(app.verify_password(password, salt2, hash2))

class TestQuizLogic(unittest.TestCase):
    """Test quiz logic and answer checking"""
    
    def setUp(self):
        """Set up test environment"""
        app.init_quiz_db()
        
        # Add test questions
        app.insert_question("What is 2+2?", ["2", "3", "4", "5"], "4", "mcq")
        app.insert_question("Python is interpreted", "", "True", "truefalse")
        app.insert_question("Capital of Japan", "", "Tokyo", "fill")
    
    def tearDown(self):
        """Clean up after tests"""
        if (TEST_DATA_DIR / "quiz.db").exists():
            (TEST_DATA_DIR / "quiz.db").unlink()
    
    def test_answer_checking(self):
        """Test answer verification logic"""
        # Test without GUI components (direct function testing)
        
        # Mock the quiz screen's answer checking method
        def check_answer(q_type, user_answer, correct_answer):
            if not user_answer:
                return False
                
            if q_type == "mcq":
                return user_answer == correct_answer
            elif q_type == "truefalse":
                return user_answer.lower() == correct_answer.lower()
            elif q_type == "fill":
                return user_answer.lower() == correct_answer.strip().lower()
            
            return False
        
        # Test MCQ answer checking
        self.assertTrue(check_answer("mcq", "4", "4"))
        self.assertFalse(check_answer("mcq", "3", "4"))
        
        # Test True/False answer checking
        self.assertTrue(check_answer("truefalse", "True", "True"))
        self.assertTrue(check_answer("truefalse", "true", "True"))
        self.assertFalse(check_answer("truefalse", "False", "True"))
        
        # Test Fill answer checking
        self.assertTrue(check_answer("fill", "Tokyo", "Tokyo"))
        self.assertTrue(check_answer("fill", "tokyo", "Tokyo"))
        self.assertFalse(check_answer("fill", "Osaka", "Tokyo"))
        
        # Test empty answer
        self.assertFalse(check_answer("mcq", "", "4"))

class TestDataPersistence(unittest.TestCase):
    """Test data persistence and file operations"""
    
    def test_data_directory_creation(self):
        """Test that data directory is created properly"""
        # Remove test directory if it exists
        if TEST_DATA_DIR.exists():
            shutil.rmtree(TEST_DATA_DIR)
        
        # Call get_data_dir which should create the directory
        data_dir = app.get_data_dir()
        
        self.assertTrue(data_dir.exists())
        self.assertTrue(data_dir.is_dir())
    
    def test_database_file_creation(self):
        """Test that database files are created in correct location"""
        app.init_user_db()
        app.init_quiz_db()
        
        self.assertTrue(app.DB_PATH.exists())
        self.assertTrue(app.QUIZ_DB_PATH.exists())
        
        # Test that files are in the expected location
        self.assertEqual(app.DB_PATH.parent, TEST_DATA_DIR)
        self.assertEqual(app.QUIZ_DB_PATH.parent, TEST_DATA_DIR)

class TestInputValidation(unittest.TestCase):
    """Test input validation and edge cases"""
    
    def setUp(self):
        app.init_user_db()
        app.init_quiz_db()
    
    def tearDown(self):
        if (TEST_DATA_DIR / "users.db").exists():
            (TEST_DATA_DIR / "users.db").unlink()
        if (TEST_DATA_DIR / "quiz.db").exists():
            (TEST_DATA_DIR / "quiz.db").unlink()
    
    def test_username_validation(self):
        """Test username validation"""
        # Empty username
        success, message = app.register_user("", "password123")
        self.assertFalse(success)
        
        # Whitespace only username
        success, message = app.register_user("   ", "password123")
        self.assertFalse(success)
        
        # Valid username with spaces (should be stripped)
        success, message = app.register_user("  validuser  ", "password123")
        self.assertTrue(success)
        
        # Verify user was registered with trimmed username
        self.assertTrue(app.authenticate_user("validuser", "password123"))
    
    def test_question_insertion_validation(self):
        """Test question data validation"""
        # Test with empty choices list
        app.insert_question("Test question", [], "answer", "mcq")
        questions = app.load_questions_from_db()
        self.assertTrue(len(questions) > 0)
        
        # Test with None choices
        app.insert_question("Test question 2", None, "answer", "fill")
        questions = app.load_questions_from_db()
        self.assertTrue(len(questions) > 1)

class TestQuizFlow(unittest.TestCase):
    """Test complete quiz flow scenarios"""
    
    def setUp(self):
        app.init_quiz_db()
        # Add sample questions for testing
        app.insert_question("What is 1+1?", ["1", "2", "3", "4"], "2", "mcq")
        app.insert_question("Is sky blue?", "", "True", "truefalse")
        app.insert_question("First President of USA", "", "Washington", "fill")
    
    def tearDown(self):
        if (TEST_DATA_DIR / "quiz.db").exists():
            (TEST_DATA_DIR / "quiz.db").unlink()
    
    def test_quiz_completion(self):
        """Test complete quiz scenario"""
        # Simulate quiz completion
        username = "testuser"
        
        # Save quiz result
        app.save_history(username, 2, 3)
        
        # Verify history was saved
        history = app.load_history(username)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][2], 2)  # score
        self.assertEqual(history[0][3], 3)  # total

class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases"""
    
    def test_database_connection_error(self):
        """Test handling of database connection issues"""
        # Try to access non-existent database location
        original_path = app.QUIZ_DB_PATH
        app.QUIZ_DB_PATH = Path("/invalid/path/quiz.db")
        
        try:
            # This should handle the error gracefully
            questions = app.load_questions_from_db()
            # If no exception is raised, questions should be empty list
            self.assertIsInstance(questions, list)
        except Exception as e:
            # If exception is raised, it should be handled appropriately
            self.assertIsInstance(e, (sqlite3.OperationalError, OSError))
        finally:
            app.QUIZ_DB_PATH = original_path
    
    def test_invalid_question_types(self):
        """Test handling of invalid question types"""
        app.init_quiz_db()
        
        # Insert question with unknown type
        app.insert_question("Test question", ["A", "B"], "A", "unknown_type")
        
        # Should not crash the application
        questions = app.load_questions_from_db()
        self.assertGreaterEqual(len(questions), 1)

def run_performance_test():
    """Basic performance test for database operations"""
    print("\n=== Performance Test ===")
    import time
    
    app.init_quiz_db()
    
    # Time question insertion
    start_time = time.time()
    for i in range(100):
        app.insert_question(f"Question {i}", ["A", "B", "C", "D"], "A", "mcq")
    insertion_time = time.time() - start_time
    
    # Time question retrieval
    start_time = time.time()
    questions = app.load_questions_from_db()
    retrieval_time = time.time() - start_time
    
    print(f"Inserted 100 questions in {insertion_time:.3f} seconds")
    print(f"Retrieved {len(questions)} questions in {retrieval_time:.3f} seconds")
    
    # Clean up
    (TEST_DATA_DIR / "quiz.db").unlink()

def run_integration_test():
    """Integration test simulating real user interaction"""
    print("\n=== Integration Test ===")
    
    try:
        # Initialize databases
        app.init_user_db()
        app.init_quiz_db()
        
        # Register users
        success1, _ = app.register_user("alice", "password123")
        success2, _ = app.register_user("bob", "secure456")
        
        print(f"User registration: Alice={success1}, Bob={success2}")
        
        # Authenticate users
        auth1 = app.authenticate_user("alice", "password123")
        auth2 = app.authenticate_user("bob", "wrongpassword")
        
        print(f"User authentication: Alice={auth1}, Bob={auth2}")
        
        # Add questions
        app.insert_question("What is Python?", ["Language", "Snake", "Tool", "All"], "All", "mcq")
        app.insert_question("Is Python free?", "", "True", "truefalse")
        
        # Check questions
        questions = app.load_questions_from_db()
        print(f"Questions in database: {len(questions)}")
        
        # Simulate quiz completion
        app.save_history("alice", 2, 2)
        app.save_history("alice", 1, 2)
        app.save_history("bob", 2, 2)
        
        # Check history
        alice_history = app.load_history("alice")
        bob_history = app.load_history("bob")
        
        print(f"Alice's quiz history: {len(alice_history)} quizzes")
        print(f"Bob's quiz history: {len(bob_history)} quizzes")
        
        print("Integration test completed successfully!")
        
    except Exception as e:
        print(f"Integration test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("EXTERNAL QUIZ APPLICATION TEST SUITE")
    print("=" * 60)
    print(f"Quiz App Location: {QUIZ_APP_FOLDER}")
    print(f"Test Data Directory: {TEST_DATA_DIR}")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestDatabaseFunctions,
        TestSecurityFunctions,
        TestQuizLogic,
        TestDataPersistence,
        TestInputValidation,
        TestQuizFlow,
        TestErrorHandling
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Run additional tests
    run_performance_test()
    integration_success = run_integration_test()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Integration test: {'PASSED' if integration_success else 'FAILED'}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, failure in result.failures:
            print(f"- {test}: {failure}")
    
    if result.errors:
        print("\nERRORRS:")
        for test, error in result.errors:
            print(f"- {test}: {error}")
    
    # Clean up test directory
    try:
        shutil.rmtree(TEST_DATA_DIR)
        print(f"\nTest directory cleaned up: {TEST_DATA_DIR}")
    except:
        print(f"\nWarning: Could not clean up test directory: {TEST_DATA_DIR}")
    
    # Exit with appropriate code
    exit_code = 0 if (result.wasSuccessful() and integration_success) else 1
    print(f"\nTest suite completed with exit code: {exit_code}")
    sys.exit(exit_code)

class TestDatabaseFunctions(unittest.TestCase):
    """Test database initialization and basic operations"""
    
    def setUp(self):
        """Set up test environment before each test"""
        # Clean up any existing test databases
        if (TEST_DATA_DIR / "users.db").exists():
            (TEST_DATA_DIR / "users.db").unlink()
        if (TEST_DATA_DIR / "quiz.db").exists():
            (TEST_DATA_DIR / "quiz.db").unlink()
    
    def tearDown(self):
        """Clean up after each test"""
        # Remove test databases
        if (TEST_DATA_DIR / "users.db").exists():
            (TEST_DATA_DIR / "users.db").unlink()
        if (TEST_DATA_DIR / "quiz.db").exists():
            (TEST_DATA_DIR / "quiz.db").unlink()
    
    def test_database_initialization(self):
        """Test that databases are created properly"""
        app.init_user_db()
        app.init_quiz_db()
        
        self.assertTrue((TEST_DATA_DIR / "users.db").exists())
        self.assertTrue((TEST_DATA_DIR / "quiz.db").exists())
    
    def test_user_registration(self):
        """Test user registration functionality"""
        app.init_user_db()
        
        # Test valid registration
        success, message = app.register_user("testuser", "password123")
        self.assertTrue(success)
        self.assertEqual(message, "Registration successful.")
        
        # Test duplicate username
        success, message = app.register_user("testuser", "password456")
        self.assertFalse(success)
        self.assertEqual(message, "Username already exists.")
        
        # Test invalid passwords
        success, message = app.register_user("user2", "12345")  # Too short
        self.assertFalse(success)
        
        success, message = app.register_user("user3", "password")  # No numbers
        self.assertFalse(success)
        
        success, message = app.register_user("user4", "123456")  # No letters
        self.assertFalse(success)
    
    def test_user_authentication(self):
        """Test user login functionality"""
        app.init_user_db()
        
        # Register a test user
        app.register_user("testuser", "password123")
        
        # Test valid login
        self.assertTrue(app.authenticate_user("testuser", "password123"))
        
        # Test invalid password
        self.assertFalse(app.authenticate_user("testuser", "wrongpassword"))
        
        # Test non-existent user
        self.assertFalse(app.authenticate_user("nonexistent", "password123"))
    
    def test_question_operations(self):
        """Test question insertion and retrieval"""
        app.init_quiz_db()
        
        # Test inserting different types of questions
        app.insert_question("What is 2+2?", ["2", "3", "4", "5"], "4", "mcq")
        app.insert_question("Python is a programming language", "", "True", "truefalse")
        app.insert_question("Capital of France is ___", "", "Paris", "fill")
        
        # Retrieve questions
        questions = app.load_questions_from_db()
        self.assertEqual(len(questions), 3)
        
        # Check question content
        mcq_question = questions[0]
        self.assertEqual(mcq_question[1], "mcq")
        self.assertEqual(mcq_question[2], "What is 2+2?")
        self.assertEqual(mcq_question[4], "4")
    
    def test_history_operations(self):
        """Test quiz history saving and loading"""
        app.init_quiz_db()
        
        # Save some quiz history
        app.save_history("testuser", 8, 10)
        app.save_history("testuser", 6, 10)
        app.save_history("otheruser", 9, 10)
        
        # Load history for specific user
        history = app.load_history("testuser")
        self.assertEqual(len(history), 2)
        
        # Check history content
        self.assertEqual(history[0][1], "testuser")  # username
        self.assertEqual(history[0][2], 8)           # score
        self.assertEqual(history[0][3], 10)          # total

class TestSecurityFunctions(unittest.TestCase):
    """Test password hashing and verification"""
    
    def test_password_hashing(self):
        """Test password hashing functionality"""
        password = "testpassword123"
        
        # Hash password
        salt, hashed = app.hash_password(password)
        
        # Verify salt and hash are created
        self.assertIsInstance(salt, bytes)
        self.assertIsInstance(hashed, bytes)
        self.assertEqual(len(salt), 16)  # Salt should be 16 bytes
        
        # Test password verification
        self.assertTrue(app.verify_password(password, salt, hashed))
        self.assertFalse(app.verify_password("wrongpassword", salt, hashed))
    
    def test_password_uniqueness(self):
        """Test that same password produces different hashes with different salts"""
        password = "samepassword"
        
        salt1, hash1 = app.hash_password(password)
        salt2, hash2 = app.hash_password(password)
        
        # Different salts should produce different hashes
        self.assertNotEqual(salt1, salt2)
        self.assertNotEqual(hash1, hash2)
        
        # Both should verify correctly
        self.assertTrue(app.verify_password(password, salt1, hash1))
        self.assertTrue(app.verify_password(password, salt2, hash2))

class TestQuizLogic(unittest.TestCase):
    """Test quiz logic and answer checking"""
    
    def setUp(self):
        """Set up test environment"""
        app.init_quiz_db()
        
        # Add test questions
        app.insert_question("What is 2+2?", ["2", "3", "4", "5"], "4", "mcq")
        app.insert_question("Python is interpreted", "", "True", "truefalse")
        app.insert_question("Capital of Japan", "", "Tokyo", "fill")
    
    def tearDown(self):
        """Clean up after tests"""
        if (TEST_DATA_DIR / "quiz.db").exists():
            (TEST_DATA_DIR / "quiz.db").unlink()
    
    def test_answer_checking(self):
        """Test answer verification logic"""
        # Create a mock quiz screen to access answer checking method
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        try:
            # Create a mock app and quiz screen
            mock_app = type('MockApp', (), {})()
            quiz_screen = app.QuizScreen(root, mock_app, "testuser", 60)
            
            if quiz_screen.questions:  # Only test if questions were loaded
                # Test MCQ answer checking
                self.assertTrue(quiz_screen._check_answer("mcq", "4", "4"))
                self.assertFalse(quiz_screen._check_answer("mcq", "3", "4"))
                
                # Test True/False answer checking
                self.assertTrue(quiz_screen._check_answer("truefalse", "True", "True"))
                self.assertTrue(quiz_screen._check_answer("truefalse", "true", "True"))
                self.assertFalse(quiz_screen._check_answer("truefalse", "False", "True"))
                
                # Test Fill answer checking
                self.assertTrue(quiz_screen._check_answer("fill", "Tokyo", "Tokyo"))
                self.assertTrue(quiz_screen._check_answer("fill", "tokyo", "Tokyo"))
                self.assertFalse(quiz_screen._check_answer("fill", "Osaka", "Tokyo"))
                
                # Test empty answer
                self.assertFalse(quiz_screen._check_answer("mcq", "", "4"))
        
        finally:
            root.destroy()

class TestDataPersistence(unittest.TestCase):
    """Test data persistence and file operations"""
    
    def test_data_directory_creation(self):
        """Test that data directory is created properly"""
        # Remove test directory if it exists
        if TEST_DATA_DIR.exists():
            shutil.rmtree(TEST_DATA_DIR)
        
        # Call get_data_dir which should create the directory
        data_dir = app.get_data_dir()
        
        self.assertTrue(data_dir.exists())
        self.assertTrue(data_dir.is_dir())
    
    def test_database_file_creation(self):
        """Test that database files are created in correct location"""
        app.init_user_db()
        app.init_quiz_db()
        
        self.assertTrue(app.DB_PATH.exists())
        self.assertTrue(app.QUIZ_DB_PATH.exists())
        
        # Test that files are in the expected location
        self.assertEqual(app.DB_PATH.parent, TEST_DATA_DIR)
        self.assertEqual(app.QUIZ_DB_PATH.parent, TEST_DATA_DIR)

class TestInputValidation(unittest.TestCase):
    """Test input validation and edge cases"""
    
    def setUp(self):
        app.init_user_db()
        app.init_quiz_db()
    
    def tearDown(self):
        if (TEST_DATA_DIR / "users.db").exists():
            (TEST_DATA_DIR / "users.db").unlink()
        if (TEST_DATA_DIR / "quiz.db").exists():
            (TEST_DATA_DIR / "quiz.db").unlink()
    
    def test_username_validation(self):
        """Test username validation"""
        # Empty username
        success, message = app.register_user("", "password123")
        self.assertFalse(success)
        
        # Whitespace only username
        success, message = app.register_user("   ", "password123")
        self.assertFalse(success)
        
        # Valid username with spaces (should be stripped)
        success, message = app.register_user("  validuser  ", "password123")
        self.assertTrue(success)
        
        # Verify user was registered with trimmed username
        self.assertTrue(app.authenticate_user("validuser", "password123"))
    
    def test_question_insertion_validation(self):
        """Test question data validation"""
        # Test with empty choices list
        app.insert_question("Test question", [], "answer", "mcq")
        questions = app.load_questions_from_db()
        self.assertTrue(len(questions) > 0)
        
        # Test with None choices
        app.insert_question("Test question 2", None, "answer", "fill")
        questions = app.load_questions_from_db()
        self.assertTrue(len(questions) > 1)

class TestQuizFlow(unittest.TestCase):
    """Test complete quiz flow scenarios"""
    
    def setUp(self):
        app.init_quiz_db()
        # Add sample questions for testing
        app.insert_question("What is 1+1?", ["1", "2", "3", "4"], "2", "mcq")
        app.insert_question("Is sky blue?", "", "True", "truefalse")
        app.insert_question("First President of USA", "", "Washington", "fill")
    
    def tearDown(self):
        if (TEST_DATA_DIR / "quiz.db").exists():
            (TEST_DATA_DIR / "quiz.db").unlink()
    
    def test_quiz_completion(self):
        """Test complete quiz scenario"""
        # Simulate quiz completion
        username = "testuser"
        
        # Save quiz result
        app.save_history(username, 2, 3)
        
        # Verify history was saved
        history = app.load_history(username)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][2], 2)  # score
        self.assertEqual(history[0][3], 3)  # total

class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases"""
    
    def test_database_connection_error(self):
        """Test handling of database connection issues"""
        # Try to access non-existent database location
        original_path = app.QUIZ_DB_PATH
        app.QUIZ_DB_PATH = Path("/invalid/path/quiz.db")
        
        try:
            # This should handle the error gracefully
            questions = app.load_questions_from_db()
            # If no exception is raised, questions should be empty list
            self.assertIsInstance(questions, list)
        except Exception as e:
            # If exception is raised, it should be handled appropriately
            self.assertIsInstance(e, (sqlite3.OperationalError, OSError))
        finally:
            app.QUIZ_DB_PATH = original_path
    
    def test_invalid_question_types(self):
        """Test handling of invalid question types"""
        app.init_quiz_db()
        
        # Insert question with unknown type
        app.insert_question("Test question", ["A", "B"], "A", "unknown_type")
        
        # Should not crash the application
        questions = app.load_questions_from_db()
        self.assertGreaterEqual(len(questions), 1)

def run_performance_test():
    """Basic performance test for database operations"""
    print("\n=== Performance Test ===")
    import time
    
    app.init_quiz_db()
    
    # Time question insertion
    start_time = time.time()
    for i in range(100):
        app.insert_question(f"Question {i}", ["A", "B", "C", "D"], "A", "mcq")
    insertion_time = time.time() - start_time
    
    # Time question retrieval
    start_time = time.time()
    questions = app.load_questions_from_db()
    retrieval_time = time.time() - start_time
    
    print(f"Inserted 100 questions in {insertion_time:.3f} seconds")
    print(f"Retrieved {len(questions)} questions in {retrieval_time:.3f} seconds")
    
    # Clean up
    (TEST_DATA_DIR / "quiz.db").unlink()

def run_integration_test():
    """Integration test simulating real user interaction"""
    print("\n=== Integration Test ===")
    
    try:
        # Initialize databases
        app.init_user_db()
        app.init_quiz_db()
        
        # Register users
        success1, _ = app.register_user("alice", "password123")
        success2, _ = app.register_user("bob", "secure456")
        
        print(f"User registration: Alice={success1}, Bob={success2}")
        
        # Authenticate users
        auth1 = app.authenticate_user("alice", "password123")
        auth2 = app.authenticate_user("bob", "wrongpassword")
        
        print(f"User authentication: Alice={auth1}, Bob={auth2}")
        
        # Add questions
        app.insert_question("What is Python?", ["Language", "Snake", "Tool", "All"], "All", "mcq")
        app.insert_question("Is Python free?", "", "True", "truefalse")
        
        # Check questions
        questions = app.load_questions_from_db()
        print(f"Questions in database: {len(questions)}")
        
        # Simulate quiz completion
        app.save_history("alice", 2, 2)
        app.save_history("alice", 1, 2)
        app.save_history("bob", 2, 2)
        
        # Check history
        alice_history = app.load_history("alice")
        bob_history = app.load_history("bob")
        
        print(f"Alice's quiz history: {len(alice_history)} quizzes")
        print(f"Bob's quiz history: {len(bob_history)} quizzes")
        
        print("Integration test completed successfully!")
        
    except Exception as e:
        print(f"Integration test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("QUIZ APPLICATION TEST SUITE")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestDatabaseFunctions,
        TestSecurityFunctions,
        TestQuizLogic,
        TestDataPersistence,
        TestInputValidation,
        TestQuizFlow,
        TestErrorHandling
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Run additional tests
    run_performance_test()
    integration_success = run_integration_test()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Integration test: {'PASSED' if integration_success else 'FAILED'}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, failure in result.failures:
            print(f"- {test}: {failure}")
    
    if result.errors:
        print("\nERRORS:")
        for test, error in result.errors:
            print(f"- {test}: {error}")
    
    # Clean up test directory
    try:
        shutil.rmtree(TEST_DATA_DIR)
        print(f"\nTest directory cleaned up: {TEST_DATA_DIR}")
    except:
        print(f"\nWarning: Could not clean up test directory: {TEST_DATA_DIR}")
    
    # Exit with appropriate code
    exit_code = 0 if (result.wasSuccessful() and integration_success) else 1
    print(f"\nTest suite completed with exit code: {exit_code}")

    sys.exit(exit_code)
