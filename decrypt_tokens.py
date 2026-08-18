#!/usr/bin/env python
"""
Quick script to fetch and decrypt access tokens from Supabase.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import KYCApplication
from encryption import decrypt_value

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("❌ DATABASE_URL not set in .env")
    exit(1)

# Connect to database
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Fetch all KYC applications ordered by most recent
applications = db.query(KYCApplication).order_by(KYCApplication.created_at.desc()).all()

if not applications:
    print("❌ No applications found in database")
    db.close()
    exit(1)

print(f"\n🔍 Found {len(applications)} applications\n")
print("=" * 100)

for idx, app in enumerate(applications, 1):
    print(f"\n#{idx} Application ID: {app.id}")
    print(f"   Created: {app.created_at}")
    print(f"   Name: {app.full_name}")
    print(f"   Status: {app.status}")
    
    if app.digilocker_access_token:
        # Decrypt the token
        decrypted_token = decrypt_value(app.digilocker_access_token) if app.digilocker_access_token else None
        print(f"   ✅ Access Token (DECRYPTED):")
        print(f"      {decrypted_token}")
    else:
        print(f"   ❌ No access token stored")
    
    print(f"   " + "-" * 96)

print("\n" + "=" * 100)
db.close()
print("\n✅ Done!")
