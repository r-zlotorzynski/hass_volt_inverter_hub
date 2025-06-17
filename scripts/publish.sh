# Install GitHub CLI
brew install gh
gh auth login


# Create a new repository on GitHub
git commit -am "Release 1.0.1"
git tag -a v1.0.0 -m "Release v1.0.1"
git push origin main
git push origin v1.0.1
gh release create v1.0.1 --notes "Add translations" --title "v1.0.1"