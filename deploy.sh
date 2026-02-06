#!/bin/bash
# Run this in your terminal after: gh auth login (once) and optionally start Docker Desktop
set -e
cd "$(dirname "$0")"

echo "=== Git status ==="
git status -s

echo ""
echo "=== Pushing to GitHub ==="
if ! git remote get-url origin 2>/dev/null; then
  echo "No GitHub remote yet. Choose one:"
  echo "  A) Create repo on GitHub (github.com/new), name it 'funding-finder', then run:"
  echo "     git remote add origin https://github.com/YOUR_USERNAME/funding-finder.git"
  echo "     git push -u origin main"
  echo "  B) Or run:  gh auth login   then run this script again (will create repo and push)"
  if command -v gh &>/dev/null && gh auth status &>/dev/null; then
    gh repo create funding-finder --public --source=. --remote=origin --push --description "Funding Finder - match users to funding opportunities"
    echo "Repo created and pushed."
  fi
else
  git push -u origin main
  echo "Pushed to GitHub."
fi

echo ""
echo "=== Docker build (optional; start Docker Desktop first) ==="
if docker info &>/dev/null 2>&1; then
  docker build -t funding-finder .
  echo "Image built: funding-finder"
else
  echo "Docker not running. Start Docker Desktop, then run: docker build -t funding-finder ."
fi

echo ""
echo "Done. Deploy at railway.app by connecting your GitHub repo."
