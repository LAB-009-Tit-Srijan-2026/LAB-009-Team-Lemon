#!/usr/bin/env node

/**
 * Alexandria Deployment Validator
 * Checks if project is ready for deployment
 */

const fs = require('fs');
const path = require('path');

const RESET = '\x1b[0m';
const GREEN = '\x1b[32m';
const RED = '\x1b[31m';
const YELLOW = '\x1b[33m';
const BLUE = '\x1b[34m';

function log(color, message) {
  console.log(`${color}${message}${RESET}`);
}

function checkFile(filePath, description) {
  const exists = fs.existsSync(filePath);
  if (exists) {
    log(GREEN, `✓ ${description}`);
  } else {
    log(RED, `✗ ${description} - NOT FOUND: ${filePath}`);
  }
  return exists;
}

function checkJson(filePath, description) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    JSON.parse(content);
    log(GREEN, `✓ ${description}`);
    return true;
  } catch (e) {
    log(RED, `✗ ${description} - INVALID JSON: ${e.message}`);
    return false;
  }
}

function checkFileContent(filePath, searchString, description) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    if (content.includes(searchString)) {
      log(GREEN, `✓ ${description}`);
      return true;
    } else {
      log(YELLOW, `⚠ ${description} - NOT FOUND in file`);
      return false;
    }
  } catch (e) {
    log(RED, `✗ ${description} - ERROR: ${e.message}`);
    return false;
  }
}

console.clear();
log(BLUE, '\n🚀 Alexandria Deployment Validator\n');

let passed = 0;
let total = 0;

// Configuration Files
log(BLUE, '📋 Configuration Files:');
total += 3;
if (checkFile('./vercel.json', 'vercel.json exists')) passed++;
if (checkFile('./.vercelignore', '.vercelignore exists')) passed++;
if (checkFile('./render.yaml', 'render.yaml exists')) passed++;

// Frontend Configuration
log(BLUE, '\n🎨 Frontend Configuration:');
total += 4;
if (checkJson('./frontend/package.json', 'frontend/package.json is valid')) passed++;
if (checkJson('./frontend/vite.config.js', 'frontend/vite.config.js syntax check')) passed++;
if (checkFile('./frontend/.env.example', 'frontend/.env.example exists')) passed++;
if (checkFileContent('./frontend/src/api/client.js', 'VITE_API_BASE_URL', 'API client uses environment variables')) passed++;

// Backend Configuration
log(BLUE, '\n🐍 Backend Configuration:');
total += 3;
if (checkFile('./backend/requirements.txt', 'backend/requirements.txt exists')) passed++;
if (checkFile('./backend/.env.example', 'backend/.env.example exists')) passed++;
if (checkFileContent('./backend/main.py', 'CORSMiddleware', 'FastAPI has CORS middleware')) passed++;

// Documentation
log(BLUE, '\n📚 Documentation:');
total += 4;
if (checkFile('./DEPLOYMENT.md', 'DEPLOYMENT.md guide exists')) passed++;
if (checkFile('./DEPLOYMENT_CHECKLIST.md', 'DEPLOYMENT_CHECKLIST.md exists')) passed++;
if (checkFile('./ENV_SETUP_GUIDE.md', 'ENV_SETUP_GUIDE.md exists')) passed++;
if (checkFile('./README.md', 'README.md exists')) passed++;

// Git Configuration
log(BLUE, '\n📦 Git Configuration:');
total += 1;
if (checkFile('./.gitignore', '.gitignore exists')) passed++;

// Summary
console.log('\n' + '='.repeat(50));
log(BLUE, `\n✅ Deployment Readiness: ${passed}/${total} checks passed\n`);

if (passed === total) {
  log(GREEN, '🎉 Project is ready for deployment!\n');
  log(YELLOW, 'Next steps:');
  log(YELLOW, '1. Read DEPLOYMENT.md for detailed instructions');
  log(YELLOW, '2. Set up API keys (see ENV_SETUP_GUIDE.md)');
  log(YELLOW, '3. Deploy frontend to Vercel');
  log(YELLOW, '4. Deploy backend to Render/Railway/Heroku');
  log(YELLOW, '5. Connect frontend to backend');
  process.exit(0);
} else {
  log(RED, '⚠️  Some issues found. Please fix them before deploying.\n');
  log(YELLOW, 'Missing items:');
  log(YELLOW, `- ${total - passed} configuration/documentation file(s)\n`);
  process.exit(1);
}
