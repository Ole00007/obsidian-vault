#!/usr/bin/env python3
import os
import sys

os.environ['DATABASE_URL'] = 'sqlite:///crm_dev.db'
os.environ['FLASK_ENV'] = 'development'

from crm import create_app
from crm.extensions import db

app = create_app()
with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("✓ Database initialized successfully with SQLite at crm_dev.db")
    print("✓ All models registered")
