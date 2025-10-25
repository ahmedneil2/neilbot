#!/usr/bin/env python3
"""
MongoDB User Migration Script
Migrate users from old bot database to new bot database
"""

from pymongo import MongoClient
import asyncio
from motor import motor_asyncio
from database.users_chats_db import db
from info import USER_DB_URI, DATABASE_NAME

# পুরাতন bot এর database configuration
OLD_DB_URI = "YOUR_OLD_BOT_MONGODB_URI"  # পুরাতন bot এর MongoDB URI এখানে দিন
OLD_DB_NAME = "YOUR_OLD_DATABASE_NAME"  # পুরাতন database এর নাম দিন
OLD_COLLECTION_NAME = "users"  # পুরাতন bot এ user collection এর নাম (সাধারণত 'users')

async def migrate_users():
    """Migrate users from old database to new database"""
    
    print("🔄 Starting user migration...")
    print(f"📂 Source: {OLD_DB_NAME}")
    print(f"📁 Target: {DATABASE_NAME}")
    print("-" * 50)
    
    # পুরাতন database connection
    old_client = motor_asyncio.AsyncIOMotorClient(OLD_DB_URI)
    old_db = old_client[OLD_DB_NAME]
    old_users = old_db[OLD_COLLECTION_NAME]
    
    # Statistics
    total_users = 0
    migrated_users = 0
    skipped_users = 0
    errors = 0
    
    try:
        # Get total count
        total_users = await old_users.count_documents({})
        print(f"📊 Total users found in old database: {total_users}")
        print("-" * 50)
        
        # Migrate each user
        async for user in old_users.find({}):
            try:
                user_id = user.get('id') or user.get('_id')
                user_name = user.get('name') or user.get('first_name') or "Unknown"
                
                if not user_id:
                    print(f"⚠️  Skipping user with no ID")
                    skipped_users += 1
                    continue
                
                # Check if user already exists
                if await db.is_user_exist(user_id):
                    print(f"⏭️  User {user_id} ({user_name}) already exists - skipping")
                    skipped_users += 1
                    continue
                
                # Add user to new database
                await db.add_user(user_id, user_name)
                migrated_users += 1
                print(f"✅ Migrated: {user_id} - {user_name}")
                
                # Optional: Migrate additional user data if exists
                # Ban status
                if 'ban_status' in user:
                    if user['ban_status'].get('is_banned'):
                        await db.ban_user(
                            user_id, 
                            user['ban_status'].get('ban_reason', 'No Reason')
                        )
                        print(f"   ⛔ Ban status migrated for {user_id}")
                
                # Premium data
                if 'expiry_time' in user and user['expiry_time']:
                    user_data = {
                        'id': user_id,
                        'expiry_time': user['expiry_time'],
                        'has_free_trial': user.get('has_free_trial', False),
                        'daily_requests': user.get('daily_requests', 0),
                        'total_requests': user.get('total_requests', 0),
                        'max_daily_requests': user.get('max_daily_requests', 10)
                    }
                    await db.update_user(user_data)
                    print(f"   💎 Premium data migrated for {user_id}")
                
                # Thumbnail
                if 'file_id' in user and user['file_id']:
                    await db.set_thumbnail(user_id, user['file_id'])
                    print(f"   🖼️  Thumbnail migrated for {user_id}")
                
                # Caption
                if 'caption' in user and user['caption']:
                    await db.set_caption(user_id, user['caption'])
                    print(f"   📝 Caption migrated for {user_id}")
                    
            except Exception as e:
                errors += 1
                print(f"❌ Error migrating user {user.get('id', 'Unknown')}: {str(e)}")
                continue
        
        print("-" * 50)
        print("📊 Migration Summary:")
        print(f"   Total users in old DB: {total_users}")
        print(f"   ✅ Successfully migrated: {migrated_users}")
        print(f"   ⏭️  Skipped (already exist): {skipped_users}")
        print(f"   ❌ Errors: {errors}")
        print("-" * 50)
        
        if errors == 0 and migrated_users > 0:
            print("✨ Migration completed successfully!")
        elif migrated_users == 0:
            print("⚠️  No new users were migrated")
        else:
            print("⚠️  Migration completed with some errors")
            
    except Exception as e:
        print(f"❌ Fatal error during migration: {str(e)}")
    finally:
        old_client.close()
        print("\n🔒 Database connections closed")

async def verify_migration():
    """Verify migration results"""
    print("\n" + "=" * 50)
    print("🔍 Verifying Migration...")
    print("=" * 50)
    
    try:
        # পুরাতন database connection
        old_client = motor_asyncio.AsyncIOMotorClient(OLD_DB_URI)
        old_db = old_client[OLD_DB_NAME]
        old_users = old_db[OLD_COLLECTION_NAME]
        
        old_count = await old_users.count_documents({})
        new_count = await db.total_users_count()
        
        print(f"📊 Old database users: {old_count}")
        print(f"📊 New database users: {new_count}")
        
        if new_count >= old_count:
            print("✅ Verification passed! All users migrated successfully")
        else:
            print(f"⚠️  Warning: New database has fewer users ({new_count - old_count} difference)")
        
        old_client.close()
        
    except Exception as e:
        print(f"❌ Verification error: {str(e)}")

def main():
    """Main function"""
    print("=" * 50)
    print("🔄 MongoDB User Migration Tool")
    print("=" * 50)
    
    # Validate configuration
    if OLD_DB_URI == "YOUR_OLD_BOT_MONGODB_URI":
        print("❌ Error: Please configure OLD_DB_URI in the script")
        print("   Edit migrate_users.py and set your old database URI")
        return
    
    if OLD_DB_NAME == "YOUR_OLD_DATABASE_NAME":
        print("❌ Error: Please configure OLD_DB_NAME in the script")
        print("   Edit migrate_users.py and set your old database name")
        return
    
    print(f"✅ Configuration validated")
    print(f"   Old DB: {OLD_DB_NAME}")
    print(f"   New DB: {DATABASE_NAME}")
    print("\n⚠️  WARNING: Make sure to backup your databases before migration!")
    
    # Confirm migration
    confirm = input("\n👉 Do you want to continue? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("❌ Migration cancelled by user")
        return
    
    # Run migration
    asyncio.run(migrate_users())
    
    # Verify migration
    verify_prompt = input("\n👉 Do you want to verify migration? (yes/no): ").strip().lower()
    if verify_prompt in ['yes', 'y']:
        asyncio.run(verify_migration())

if __name__ == "__main__":
    main()
