"""
Environment Configuration Validator
Checks if all required Supabase credentials are properly configured
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

def check_env_var(name, description, is_secret=False):
    """Check if an environment variable is set and valid"""
    value = os.getenv(name, "")
    
    # Check if it's a placeholder
    placeholders = ['[PROJECT-REF]', '[YOUR-PASSWORD]', '[REGION]', 'your-', 'change-in-production']
    is_placeholder = any(p in value for p in placeholders)
    
    if not value:
        print(f"❌ {name}: NOT SET")
        print(f"   → {description}")
        return False
    elif is_placeholder:
        print(f"⚠️  {name}: PLACEHOLDER DETECTED")
        print(f"   → {description}")
        print(f"   Current: {value[:50]}...")
        return False
    else:
        if is_secret:
            print(f"✅ {name}: Configured ({len(value)} chars)")
        else:
            print(f"✅ {name}: {value[:50]}{'...' if len(value) > 50 else ''}")
        return True

def main():
    print("=" * 70)
    print("🔍 ATLAS AI - Environment Configuration Validator")
    print("=" * 70)
    
    all_valid = True
    
    print("\n📦 REQUIRED - Supabase Database")
    print("-" * 70)
    all_valid &= check_env_var(
        "DATABASE_URL",
        "Get from: Supabase Dashboard > Connect > Transaction mode (Port 6543)",
        is_secret=True
    )
    all_valid &= check_env_var(
        "SUPABASE_URL",
        "Get from: Supabase Dashboard > Project Settings > API > Project URL"
    )
    all_valid &= check_env_var(
        "SUPABASE_ANON_KEY",
        "Get from: Supabase Dashboard > Project Settings > API > anon public",
        is_secret=True
    )
    all_valid &= check_env_var(
        "SUPABASE_SERVICE_KEY",
        "Get from: Supabase Dashboard > Project Settings > API > service_role",
        is_secret=True
    )
    
    print("\n🔐 REQUIRED - Security")
    print("-" * 70)
    all_valid &= check_env_var(
        "SECRET_KEY",
        "Generate a random string for JWT signing (e.g., openssl rand -hex 32)"
    )
    
    print("\n🤖 OPTIONAL - AI Features")
    print("-" * 70)
    check_env_var(
        "OPENAI_API_KEY",
        "Get from: https://platform.openai.com/api-keys (for chatbot)"
    )
    check_env_var(
        "ONET_API_KEY",
        "Get from: https://services.onetcenter.org/reference (for career data)"
    )
    check_env_var(
        "GITHUB_TOKEN",
        "Get from: https://github.com/settings/tokens (for GitHub integration)"
    )
    
    print("\n" + "=" * 70)
    if all_valid:
        print("✨ All required configuration is valid!")
        print("=" * 70)
        print("\n📝 Next steps:")
        print("   1. Run: python setup_database.py")
        print("   2. Run: python main.py")
        print("   3. Visit: http://localhost:8000/docs")
    else:
        print("⚠️  Configuration incomplete!")
        print("=" * 70)
        print("\n📝 Action required:")
        print("   1. Open: backend/.env")
        print("   2. Follow: backend/SUPABASE_SETUP.md")
        print("   3. Update all values marked with ❌ or ⚠️")
        print("   4. Run this script again to verify")
    
    print()

if __name__ == "__main__":
    main()
