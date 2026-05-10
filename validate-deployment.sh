#!/bin/bash
# Deployment validator for Alexandria

RESET='\033[0m'
GREEN='\033[32m'
RED='\033[31m'
YELLOW='\033[33m'
BLUE='\033[34m'

echo -e "${BLUE}"
echo "🚀 Alexandria Deployment Validator"
echo -e "${RESET}"

passed=0
total=0

# Configuration Files
echo -e "${BLUE}📋 Configuration Files:${RESET}"

for file in vercel.json .vercelignore render.yaml; do
  ((total++))
  if [ -f "$file" ]; then
    echo -e "${GREEN}✓ $file exists${RESET}"
    ((passed++))
  else
    echo -e "${RED}✗ $file NOT FOUND${RESET}"
  fi
done

# Frontend Configuration
echo -e "${BLUE}\n🎨 Frontend Configuration:${RESET}"

for file in frontend/package.json frontend/.env.example; do
  ((total++))
  if [ -f "$file" ]; then
    echo -e "${GREEN}✓ $file exists${RESET}"
    ((passed++))
  else
    echo -e "${RED}✗ $file NOT FOUND${RESET}"
  fi
done

# Backend Configuration
echo -e "${BLUE}\n🐍 Backend Configuration:${RESET}"

for file in backend/requirements.txt backend/.env.example; do
  ((total++))
  if [ -f "$file" ]; then
    echo -e "${GREEN}✓ $file exists${RESET}"
    ((passed++))
  else
    echo -e "${RED}✗ $file NOT FOUND${RESET}"
  fi
done

# Documentation
echo -e "${BLUE}\n📚 Documentation:${RESET}"

for file in DEPLOYMENT.md DEPLOYMENT_CHECKLIST.md ENV_SETUP_GUIDE.md README.md; do
  ((total++))
  if [ -f "$file" ]; then
    echo -e "${GREEN}✓ $file exists${RESET}"
    ((passed++))
  else
    echo -e "${RED}✗ $file NOT FOUND${RESET}"
  fi
done

# Summary
echo -e "\n$(printf '=%.0s' {1..50})"
echo -e "${BLUE}✅ Deployment Readiness: $passed/$total checks passed${RESET}\n"

if [ $passed -eq $total ]; then
  echo -e "${GREEN}🎉 Project is ready for deployment!${RESET}\n"
  echo -e "${YELLOW}Next steps:${RESET}"
  echo -e "${YELLOW}1. Read DEPLOYMENT.md for detailed instructions${RESET}"
  echo -e "${YELLOW}2. Set up API keys (see ENV_SETUP_GUIDE.md)${RESET}"
  echo -e "${YELLOW}3. Deploy frontend to Vercel${RESET}"
  echo -e "${YELLOW}4. Deploy backend to Render/Railway/Heroku${RESET}"
  echo -e "${YELLOW}5. Connect frontend to backend${RESET}"
else
  echo -e "${RED}⚠️  Some issues found. Please fix them before deploying.${RESET}\n"
  echo -e "${YELLOW}Missing items: $((total - passed)) file(s)${RESET}"
fi
