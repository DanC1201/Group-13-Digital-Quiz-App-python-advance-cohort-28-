
QuizApp - Integrated project
============================

What I added:
- app.py : A self-contained Tkinter app with Login, Register, and Home pages.
- Uses SQLite database users.db for storing users (with PBKDF2-HMAC-SHA256 password hashing).
- If your original project had files, they were preserved in the QuizApp folder alongside app.py.
- Database file users.db will be created automatically after first run.

Run instructions:
1. Make sure you have Python 3.8+ installed.
2. From this folder run: python app.py
   (On some systems you may need: python3 app.py)

Notes on security:
- Passwords are NOT stored in plaintext. Each user gets a random salt and a hashed password computed via PBKDF2.
- For stronger compatibility with other systems, you may swap to bcrypt (requires installing 'bcrypt' package).
- This is a local desktop app; if you move to a server, consider additional protections (TLS, rate-limiting, input sanitization).

Output zip path: /mnt/data/QuizApp.zip

