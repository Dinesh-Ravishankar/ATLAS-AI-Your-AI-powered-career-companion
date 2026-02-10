# Quick GitHub Upload Script for Atlas AI
# Run this script to prepare and upload to GitHub

Write-Host "🚀 Atlas AI - GitHub Upload Preparation" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Clean temporary files
Write-Host "Step 1: Cleaning temporary files..." -ForegroundColor Yellow
$filesToDelete = @(
    "backend\atlas_ai.db",
    "backend\diag_err.txt",
    "backend\diag_out.txt",
    "backend\greenlet_test.txt",
    "backend\server_err.txt",
    "backend\server_out.txt",
    "backend\util_test.txt",
    "backend\check.txt",
    "backend\startup_log.txt",
    "backend\import_log.txt"
)

foreach ($file in $filesToDelete) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  ✓ Deleted: $file" -ForegroundColor Green
    }
}
Write-Host "  ✓ Cleanup complete!" -ForegroundColor Green
Write-Host ""

# Step 2: Initialize Git
Write-Host "Step 2: Initializing Git repository..." -ForegroundColor Yellow
git init
git branch -M main
Write-Host "  ✓ Git initialized!" -ForegroundColor Green
Write-Host ""

# Step 3: Add files
Write-Host "Step 3: Adding files to Git..." -ForegroundColor Yellow
git add .
Write-Host "  ✓ Files staged!" -ForegroundColor Green
Write-Host ""

# Step 4: Show what will be committed
Write-Host "Step 4: Files to be committed:" -ForegroundColor Yellow
Write-Host ""
git status --short
Write-Host ""

# Step 5: Security check
Write-Host "Step 5: Security check - searching for potential secrets..." -ForegroundColor Yellow
$secretPatterns = @("sk-", "OPENAI_API_KEY", "SECRET_KEY")
$foundSecrets = $false

foreach ($pattern in $secretPatterns) {
    $results = git grep -i $pattern -- ':!*.md' ':!*.example' 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ⚠️  WARNING: Found '$pattern' in code files!" -ForegroundColor Red
        Write-Host $results
        $foundSecrets = $true
    }
}

if (-not $foundSecrets) {
    Write-Host "  ✓ No secrets found in code files!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "  ⚠️  STOP! Secrets detected in files!" -ForegroundColor Red
    Write-Host "  Review the files above before continuing." -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 6: First commit
Write-Host "Step 6: Creating first commit..." -ForegroundColor Yellow
git commit -m "feat: initial commit - Atlas AI v0.9.0-beta

- Complete FastAPI backend with 43 endpoints
- React 18 + TypeScript frontend
- 13 AI modules (OpenAI, LangChain, Sentence Transformers)
- Gamification system
- Docker containerization
- Comprehensive documentation

See COMPREHENSIVE_ANALYSIS_REPORT.md for full details."

Write-Host "  ✓ First commit created!" -ForegroundColor Green
Write-Host ""

# Step 7: Instructions for GitHub
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ Local repository ready for upload!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Create a new repository on GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Repository settings:" -ForegroundColor White
Write-Host "   - Name: Atlas-AI" -ForegroundColor Gray
Write-Host "   - Description: Intelligent Career Development Platform powered by AI" -ForegroundColor Gray
Write-Host "   - Public or Private (your choice)" -ForegroundColor Gray
Write-Host "   - Do NOT initialize with README" -ForegroundColor Red
Write-Host ""
Write-Host "3. Connect and push (replace YOUR_USERNAME):" -ForegroundColor White
Write-Host ""
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/Atlas-AI.git" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "See GITHUB_UPLOAD_GUIDE.md for detailed instructions!" -ForegroundColor Yellow
Write-Host ""
