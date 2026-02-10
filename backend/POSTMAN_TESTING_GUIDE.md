# Testing Atlas AI Backend with Postman

## 📥 Step 1: Install Postman
Download from: https://www.postman.com/downloads/

## 🚀 Step 2: Test Endpoints

### ✅ Test 1: Health Check (GET)

**URL**: `http://localhost:8000/`

**Method**: `GET`

**Expected Response**:
```json
{
  "message": "Atlas AI Backend API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

### 👤 Test 2: Register User (POST)

**URL**: `http://localhost:8000/auth/register`

**Method**: `POST`

**Headers**:
```
Content-Type: application/json
```

**Body** (raw JSON):
```json
{
  "email": "john@example.com",
  "full_name": "John Doe",
  "password": "SecurePass123"
}
```

**Expected Response** (201 Created):
```json
{
  "id": 1,
  "email": "john@example.com",
  "full_name": "John Doe",
  "created_at": "2026-02-09T10:30:00"
}
```

---

### 🔐 Test 3: Login (POST)

**URL**: `http://localhost:8000/auth/login`

**Method**: `POST`

**Headers**:
```
Content-Type: application/x-www-form-urlencoded
```

**Body** (x-www-form-urlencoded):
```
username: john@example.com
password: SecurePass123
```

**Expected Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**📝 IMPORTANT**: Copy the `access_token` value for the next steps!

---

### 👥 Test 4: Get Current User (GET) - Protected Route

**URL**: `http://localhost:8000/auth/me`

**Method**: `GET`

**Headers**:
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

**Expected Response** (200 OK):
```json
{
  "id": 1,
  "email": "john@example.com",
  "full_name": "John Doe",
  "created_at": "2026-02-09T10:30:00"
}
```

---

### 📋 Test 5: Get Profile (GET)

**URL**: `http://localhost:8000/profile/me`

**Method**: `GET`

**Headers**:
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

**Expected Response** (200 OK):
```json
{
  "id": 1,
  "user_id": 1,
  "bio": null,
  "location": null,
  "target_roles": null,
  "level": 1,
  "xp": 0
}
```

---

### ✏️ Test 6: Update Profile (PUT)

**URL**: `http://localhost:8000/profile/me`

**Method**: `PUT`

**Headers**:
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
Content-Type: application/json
```

**Body** (raw JSON):
```json
{
  "bio": "Aspiring Data Scientist passionate about AI",
  "location": "San Francisco, CA",
  "github_url": "https://github.com/johndoe",
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "target_roles": ["Data Scientist", "ML Engineer"],
  "interests": ["Machine Learning", "Python", "Deep Learning"],
  "major": "Computer Science",
  "university": "Stanford University",
  "graduation_year": 2024
}
```

**Expected Response** (200 OK):
```json
{
  "id": 1,
  "user_id": 1,
  "bio": "Aspiring Data Scientist passionate about AI",
  "location": "San Francisco, CA",
  "target_roles": ["Data Scientist", "ML Engineer"],
  ...
}
```

---

## 🎯 Postman Collection Setup (Quick Method)

### Create a Collection:

1. **Open Postman** → Click "New" → "Collection"
2. **Name it**: "Atlas AI Backend"
3. **Add requests** using the steps above

### Set Up Environment Variables:

1. Click "Environments" → "Create Environment"
2. Name: "Atlas AI Local"
3. Add variables:
   - `base_url` = `http://localhost:8000`
   - `token` = (leave empty, will be set after login)

4. Use in requests:
   - URL: `{{base_url}}/auth/register`
   - Authorization: `Bearer {{token}}`

---

## 🔧 Troubleshooting

### If you get 500 Internal Server Error:

1. **Check server logs** in the terminal where `python main.py` is running
2. **Common issues**:
   - Database connection problems
   - Missing required fields
   - Validation errors

### If you get 401 Unauthorized:

- Your token expired or is invalid
- Re-login to get a new token

### If you get 422 Validation Error:

- Check your request body format
- Ensure all required fields are present
- Verify JSON syntax

---

## 📊 Testing Workflow

1. ✅ Health Check
2. ✅ Register User
3. ✅ Login (get token)
4. ✅ Get Current User (verify token works)
5. ✅ Get Profile
6. ✅ Update Profile
7. ✅ Test other endpoints as needed

---

## 🌐 Alternative: Use Swagger UI

Open in browser: **http://localhost:8000/docs**

- Interactive API documentation
- Test endpoints directly in browser
- No Postman needed!
- Click "Try it out" on any endpoint
