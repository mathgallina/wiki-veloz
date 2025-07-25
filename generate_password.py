#!/usr/bin/env python3
"""
Script to generate password hash for testing
"""

from werkzeug.security import generate_password_hash

# Test different passwords
passwords = ["admin123", "admin", "123456", "password"]

for password in passwords:
    hash_value = generate_password_hash(password)
    print(f"Password: {password}")
    print(f"Hash: {hash_value}")
    print("-" * 50) 