# Akash Animated GitHub Profile — Setup

## 1. Create the profile repository

Create a **public** repository whose name exactly matches your GitHub username. GitHub displays its root `README.md` as your profile README.

## 2. Copy this package

Copy all files into that repository.

## 3. Generate your portrait locally

Put a portrait photo in the repository root as `source-photo.jpg`.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
pip install -r scripts/requirements-local.txt
python scripts/prep_photo.py source-photo.jpg
python scripts/make_ascii_svg.py
python scripts/make_info_card.py
```

The source photo is ignored by `.gitignore`.

## 4. Generate the heatmap locally

```bash
export GITHUB_USERNAME=YOUR_GITHUB_USERNAME
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py
```

## 5. Push

```bash
git add .
git commit -m "build animated GitHub profile"
git branch -M main
git push -u origin main
```

## 6. Run Actions

Open **Actions → Update profile art → Run workflow** once. It will then refresh daily.

The workflow only installs `requests` and `beautifulsoup4`; the heavier portrait packages are local-only.

## 7. Customize

Edit `scripts/make_info_card.py` for your profile details and `README.md` for links/text.

### Important implementation note

The heatmap fetcher uses GitHub's public contribution HTML fragment at `https://github.com/users/<username>/contributions`. This is not a documented public API and its markup can change, so the parser may need maintenance if GitHub changes that page.
