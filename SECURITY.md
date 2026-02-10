# Security Policy

## 🔒 Supported Versions

Currently supported versions for security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.9.x   | :white_check_mark: |
| < 0.9   | :x:                |

## 🚨 Reporting a Vulnerability

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

1. **Private Security Advisory** (Preferred)
   - Go to the Security tab in the repository
   - Click "Report a vulnerability"
   - Follow the template

2. **Direct Email**
   - Send details to: [security@your-domain.com]
   - Include "ATLAS-AI-SECURITY" in the subject

### What to Include

Please provide:
- **Description** of the vulnerability
- **Steps to reproduce** (proof of concept)
- **Potential impact** of the vulnerability
- **Suggested fix** (if you have one)

### Response Timeline

- **Initial Response:** Within 48 hours
- **Status Update:** Within 7 days
- **Fix Timeline:** Depends on severity
  - Critical: 1-7 days
  - High: 7-30 days
  - Medium: 30-90 days
  - Low: Next release cycle

## 🛡️ Known Security Considerations

### Current Implementation (v0.9.0)

1. **API Keys & Secrets**
   - Stored in `.env` files (not committed to repo)
   - JWT tokens with HS256 algorithm
   - bcrypt for password hashing

2. **Rate Limiting**
   - ⚠️ **Not yet implemented** - vulnerable to brute force
   - Planned for v1.0.0

3. **Input Validation**
   - Pydantic schemas for API validation
   - ⚠️ File upload validation limited

4. **CORS**
   - Configured in FastAPI
   - ⚠️ May need tightening for production

5. **Dependencies**
   - Regular updates recommended
   - Run `pip audit` and `npm audit` regularly

### Security Checklist for Deployment

Before deploying to production, ensure:

- [ ] All `.env` files with real credentials are in `.gitignore`
- [ ] `SECRET_KEY` is cryptographically random (32+ bytes)
- [ ] Database credentials are secured
- [ ] HTTPS/TLS is enabled
- [ ] CORS settings match your domain
- [ ] Rate limiting is enabled
- [ ] Input validation covers all endpoints
- [ ] Dependencies are up to date
- [ ] Security headers are configured (CSP, HSTS, etc.)
- [ ] File upload size limits are set
- [ ] Error messages don't leak sensitive info
- [ ] Logging doesn't include secrets

## 🔐 Security Best Practices

### For Users

1. **Strong Passwords**
   - Minimum 8 characters
   - Mix of letters, numbers, symbols
   - Use a password manager

2. **API Keys**
   - Never commit to version control
   - Rotate regularly
   - Use environment-specific keys

3. **Updates**
   - Keep dependencies updated
   - Monitor security advisories

### For Developers

1. **Code Review**
   - All code must be reviewed before merging
   - Security-focused reviews for auth/API changes

2. **Testing**
   - Include security test cases
   - Test authentication flows thoroughly

3. **Dependencies**
   ```bash
   # Python
   pip install safety
   safety check
   
   # Node.js
   npm audit
   npm audit fix
   ```

4. **Secrets Management**
   - Never hardcode secrets
   - Use environment variables
   - Consider secrets management tools (Vault, AWS Secrets Manager)

## 📚 Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [React Security Best Practices](https://snyk.io/learn/react-security/)
- [CWE Top 25](https://cwe.mitre.org/top25/)

## 🏆 Security Hall of Fame

We recognize security researchers who responsibly disclose vulnerabilities:

(No vulnerabilities reported yet)

---

**Last Updated:** February 10, 2026  
**Policy Version:** 1.0
