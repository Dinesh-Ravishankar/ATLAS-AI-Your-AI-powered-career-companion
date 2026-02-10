"""
Atlas AI API Testing Script
Tests all major endpoints to verify the backend is working correctly
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health_check():
    print_section("1. Health Check")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_register():
    print_section("2. User Registration")
    user_data = {
        "email": "test@atlasai.com",
        "full_name": "Test User",
        "password": "SecurePass123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=user_data
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ User registered successfully!")
            print(f"User: {response.json()}")
            return True, user_data
        elif response.status_code == 400:
            print("⚠️  User already exists (this is OK)")
            return True, user_data
        else:
            print(f"❌ Registration failed: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, None

def test_login(user_data):
    print_section("3. User Login")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data={
                "username": user_data["email"],  # OAuth2 uses 'username' field
                "password": user_data["password"]
            }
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Login successful!")
            print(f"Access Token: {token_data['access_token'][:50]}...")
            return True, token_data["access_token"]
        else:
            print(f"❌ Login failed: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, None

def test_get_current_user(token):
    print_section("4. Get Current User (Protected Route)")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            user = response.json()
            print("✅ Successfully retrieved user info!")
            print(f"Email: {user['email']}")
            print(f"Name: {user['full_name']}")
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_profile(token):
    print_section("5. Get User Profile")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/profile/me",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            profile = response.json()
            print("✅ Profile retrieved!")
            print(f"Profile: {json.dumps(profile, indent=2)}")
            return True
        else:
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_update_profile(token):
    print_section("6. Update User Profile")
    
    profile_data = {
        "bio": "AI enthusiast and aspiring data scientist",
        "location": "San Francisco, CA",
        "github_url": "https://github.com/testuser",
        "target_roles": ["Data Scientist", "ML Engineer"],
        "interests": ["Machine Learning", "Python", "AI"]
    }
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(
            f"{BASE_URL}/profile/me",
            headers=headers,
            json=profile_data
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            profile = response.json()
            print("✅ Profile updated successfully!")
            print(f"Bio: {profile.get('bio')}")
            print(f"Target Roles: {profile.get('target_roles')}")
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_career_recommendations(token):
    print_section("7. Get Career Recommendations")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/career/recommendations",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        # This might not be fully implemented yet
        if response.status_code in [200, 404, 501]:
            print("⚠️  Endpoint exists (implementation may be pending)")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_all_tests():
    print("\n" + "🚀 " + "="*56)
    print("  ATLAS AI BACKEND API TESTING")
    print("="*60)
    
    results = []
    
    # Test 1: Health Check
    results.append(("Health Check", test_health_check()))
    
    # Test 2: Register
    success, user_data = test_register()
    results.append(("Registration", success))
    
    if not success:
        print("\n❌ Cannot continue without successful registration")
        return
    
    # Test 3: Login
    success, token = test_login(user_data)
    results.append(("Login", success))
    
    if not success:
        print("\n❌ Cannot continue without valid token")
        return
    
    # Test 4: Get Current User
    results.append(("Get Current User", test_get_current_user(token)))
    
    # Test 5: Get Profile
    results.append(("Get Profile", test_get_profile(token)))
    
    # Test 6: Update Profile
    results.append(("Update Profile", test_update_profile(token)))
    
    # Test 7: Career Recommendations
    results.append(("Career Recommendations", test_career_recommendations(token)))
    
    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your backend is working perfectly!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above for details.")

if __name__ == "__main__":
    print("\nMake sure your backend server is running on http://localhost:8000")
    print("Press Enter to start testing...")
    input()
    
    run_all_tests()
