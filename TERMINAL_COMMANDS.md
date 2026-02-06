# Fix GitHub 401 and push

Your `gh` CLI isn’t logged in. Do this in order.

## Step 1: Log in to GitHub (in your terminal)

```bash
gh auth login
```

When prompted:

1. **What account do you want to log into?** → **GitHub.com**
2. **What is your preferred protocol?** → **HTTPS**
3. **Authenticate Git with your GitHub credentials?** → **Yes**
4. **How would you like to authenticate?** → **Login with a web browser** (easiest)

Copy the one-time code they show, press Enter, then in the browser paste the code and approve. When the terminal says “Logged in as …”, you’re done.

## Step 2: Create the repo and push

```bash
cd "/Users/jenniferwest/Downloads/New Folder With Items"
gh repo create funding-finder --public --source=. --remote=origin --push --description "Funding Finder - match users to funding opportunities"
```

---

## If you prefer not to use `gh`: create the repo on the website, then push

1. Open **https://github.com/new**
2. Repository name: **funding-finder**
3. Public → **Create repository**
4. In your terminal (don’t run “git init” or “README” on GitHub if the repo is empty):

```bash
cd "/Users/jenniferwest/Downloads/New Folder With Items"
git remote add origin https://github.com/Jennaleighwilder/funding-finder.git
git branch -M main
git push -u origin main
```

If it asks for credentials, use your GitHub username and a **Personal Access Token** (not your password): GitHub → Settings → Developer settings → Personal access tokens → Generate new token, check **repo**, then paste the token when git asks for a password.
