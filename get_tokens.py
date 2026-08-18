#!/usr/bin/env python
"""
Decrypt access tokens from Render production database.
"""

import os
import sys

# Set encryption key from local .env
os.environ['ENCRYPTION_KEY'] = 'UtVQRBZk8DHWZZcC4Iy3IvAh--ayJl0PFM2jMXKweBA='

from sqlalchemy import create_engine, text
from encryption import decrypt_value

# Render production database
DATABASE_URL = 'postgresql://postgres.vrxmrwyyijgiyznyxcya:Nangia%40August%40@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres'

engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args={'connect_timeout': 10})

try:
    with engine.connect() as conn:
        result = conn.execute(text('SELECT COUNT(*) FROM kyc_applications'))
        count = result.fetchone()[0]
        print(f'\n📈 Total records: {count}\n')
        
        if count > 0:
            result = conn.execute(text('SELECT id, full_name, created_at, digilocker_access_token FROM kyc_applications ORDER BY created_at DESC LIMIT 5'))
            
            print('🔐 DECRYPTED ACCESS TOKENS')
            print('=' * 120)
            
            for idx, row in enumerate(result, 1):
                app_id, name, created, token = row
                print(f'\n#{idx} Application')
                print(f'    ID: {app_id}')
                print(f'    Name: {name}')
                print(f'    Created: {created}')
                
                if token:
                    try:
                        decrypted = decrypt_value(token)
                        print(f'    \n    ✅ ACCESS TOKEN:\n    {decrypted}')
                    except Exception as e:
                        print(f'    ❌ Decryption error: {e}')
                else:
                    print(f'    ❌ No token stored')
                    
                print('    ' + '-' * 116)
                
            print('\n' + '=' * 120)
            
except Exception as e:
    print(f'❌ Connection/Query Error: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
