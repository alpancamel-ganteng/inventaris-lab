# Password Hashing Security

## Project
Inventaris Lab - Secure Inventory Management System

## Implementation

The application uses Werkzeug password hashing with the scrypt method.

Password hashing is implemented in:
- Line 72: Demo user password hashing.
- Line 128: Password verification during login.
- Line 236: Password hashing when creating a new user.

## Security Mechanism

1. User passwords are hashed using scrypt.
2. Plaintext passwords are not stored in the database.
3. During login, check_password_hash() verifies the entered password against the stored hash.
4. The same hashing mechanism is used for demo users and newly created users.

## Conclusion

The application uses scrypt password hashing to protect user credentials.
This makes stored passwords safer than storing them as plaintext.
