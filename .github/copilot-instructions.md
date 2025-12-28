# Ancient Coin Collection Website - AI Coding Instructions

## Project Overview
This is a Jekyll-based coin collection showcase website, adapted from the al-folio academic theme. It displays ancient Greek and Roman coins with image galleries, detailed metadata, and filtering capabilities.

## Architecture & Key Components

### Jekyll Core Structure
- **Liquid templates** in `_includes/` and `_layouts/` render content
- **Coins collection** in `_coins/` - main content type (markdown files with coin metadata)
- **Custom coin layout** `_layouts/coin.liquid` displays individual coin pages with obverse/reverse images
- **Configuration** `_config.yml` - Central config for site metadata and collections

### Content Organization
- **Coins** (`_coins/*.md`): Individual coin entries with frontmatter metadata and descriptions
- **Pages** (`_pages/*.md`): Main site pages (home, collection, showcase, about)
- **Images** (`assets/img/coins/`): Coin photographs (obverse, reverse, details)
- **Configuration** (`_config.yml`): Site settings, collection config

### Coin Entry Format
Each coin is a markdown file in `_coins/` with this structure:

```yaml
---
layout: coin
title: "Augustus Aureus, Lugdunum"
period: Imperial              # Greek, Republican, or Imperial
ruler: Augustus
mint: Lugdunum
denomination: Aureus
date_minted: "2 BC - 4 AD"
reference: "RIC I² 207"       # Standard numismatic reference
metal: Gold
weight: "7.81g"
diameter: "19mm"
grade: "EF"                   # Numismatic grade
image: coins/augustus-lugdunum.jpg          # Obverse image
image_reverse: coins/augustus-reverse.jpg   # Optional reverse image
featured: true                # Shows in showcase gallery
tags: [augustus, lugdunum, gold]
categories: [imperial, gold]
---

Historical description and context here...
```

### Site Pages
Four main pages in `_pages/`:
- `about.md` - Homepage with collection overview
- `collection.md` - Filterable grid of all coins (JavaScript filters by period)
- `showcase.md` - Gallery of featured coins (where `featured: true`)
- `about-collection.md` - About the collection and collecting philosophy

## Development Workflows

### Local Development
**Docker (recommended):**
```bash
docker compose pull
docker compose up  # Site at http://localhost:8080
```
Slim image: `docker compose -f docker-compose-slim.yml up`

**Manual (legacy, not recommended):**
```bash
bundle install
bundle exec jekyll serve  # Site at http://localhost:4000
```

**Live reload:** Docker setup includes `--livereload` and watches `_config.yml` changes (auto-restarts Jekyll)

### Making Changes
- **Config changes** (`_config.yml`): Require Jekyll restart or rebuild
- **Content/template changes**: Auto-reload in Docker, or refresh browser
- **Before committing**: Code is auto-formatted by Prettier via GitHub Actions (`.github/workflows/prettier.yml`)

### Deployment
- **GitHub Actions** (`.github/workflows/deploy.yml`): Auto-deploys on push to main/master
- Builds site → pushes to `gh-pages` branch → GitHub Pages serves it
- Deployment takes ~4 min; then `pages-build-deployment` action (~45s) finalizes
- **Critical config**: Set `url` to `https://<username>.github.io`, leave `baseurl` empty for user/org sites

## Project-Specific Patterns

### Adding a New Coin
1. Create markdown file in `_coins/` (e.g., `hadrian_denarius.md`)
2. Add coin images to `assets/img/coins/`
3. Fill out frontmatter with metadata (see format above)
4. Write description in markdown body
5. Set `featured: true` to show in showcase gallery

### Filtering System
The collection page uses JavaScript to filter coins by period:
- Filters target `data-period` attribute on `.coin-card` elements
- Period values: `greek`, `republican`, `imperial`
- Add new filter buttons in `collection.md` and update JavaScript

### Image Display
- **Grid view**: `coin-card-image` CSS creates square containers with centered images
- **Individual pages**: Side-by-side obverse/reverse display in `coin.liquid` layout
- **Responsive**: Images scale on mobile, cards stack vertically

### Styling Conventions
- Coin-specific CSS embedded in page files (collection.md, showcase.md)
- Layout styling in `_layouts/coin.liquid`
- Uses CSS variables: `--global-theme-color`, `--global-bg-color`, `--global-text-color`
- Dark/light mode support inherited from al-folio theme

## Common Tasks

### Add Multiple Coins
1. For each coin, create `_coins/coinname.md`
2. Copy images to `assets/img/coins/`
3. Use consistent naming: lowercase, underscores (e.g., `tiberius_tribute.md`)
4. Set appropriate `period`, `categories`, and `tags` for filtering

### Customize Colors
- Theme color: Edit `--global-theme-color` in `_sass/_themes.scss`
- Period badges: Color defined in coin.liquid and collection.md styles
- Card hover effects: Modify `.coin-card:hover` in collection.md

### Update Navigation
- Edit `nav: true` and `nav_order` in page frontmatter
- Main navigation auto-generates from pages with `nav: true`
- Current pages: Collection (1), Showcase (2), About (3)

## Disabled Features

These al-folio features are turned off:
- ❌ Blog posts / pagination
- ❌ Publications / bibliography
- ❌ CV page
- ❌ News announcements  
- ❌ Projects collection
- ❌ External RSS feeds
- ❌ Social media integrations
- ❌ Comments (Giscus/Disqus)
- ❌ Newsletter signup

## Troubleshooting

### Images Not Showing
- Verify image path starts with `coins/` (relative to `/assets/img/`)
- Check file exists: `assets/img/coins/filename.jpg`
- Image paths in frontmatter shouldn't include `/assets/img/` prefix

### Filters Not Working
- Check `data-period` attribute matches filter values exactly
- Ensure JavaScript is loading (check browser console)
- Period must be lowercase: `greek`, `republican`, `imperial`

### Card Layout Issues
- Grid uses CSS Grid with `repeat(auto-fill, minmax(280px, 1fr))`
- Adjust minmax value in collection.md for different card sizes
- Cards auto-wrap on narrow screens

## Key Files Reference
- [`_config.yml`](_config.yml) - Site configuration
- [`_layouts/coin.liquid`](_layouts/coin.liquid) - Individual coin page template
- [`_pages/collection.md`](_pages/collection.md) - Main collection grid
- [`_pages/showcase.md`](_pages/showcase.md) - Featured coins gallery
- [`assets/img/coins/`](assets/img/coins/) - Coin images directory

## Additional Resources
- [Jekyll Collections](https://jekyllrb.com/docs/collections/)
- [Liquid Template Language](https://shopify.github.io/liquid/)
- [Original al-folio Theme](https://github.com/alshedivat/al-folio)
