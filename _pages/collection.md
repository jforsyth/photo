---
layout: page
title: Collection
permalink: /collection/
description: Browse the complete collection of Jason's Ancient Coins
nav: true
nav_order: 2
---

<div class="showcase-intro">
  <p></p>
</div>

<div class="showcase-gallery">
  {% assign featured_coins = site.coins | where: "featured", true %}
  {% for coin in featured_coins %}
    <div class="showcase-item">
      <a href="{{ coin.url | relative_url }}">
        {% if coin.image_aligned %}
          <img src="{{ coin.image_aligned | prepend: '/assets/img/' | relative_url }}" alt="{{ coin.title }}">
        {% elsif coin.image_obverse %}
          <img src="{{ coin.image_obverse | prepend: '/assets/img/' | relative_url }}" alt="{{ coin.title }}">
        {% endif %}
        <div class="showcase-overlay">
          <h3>{{ coin.title }}</h3>
          <p>{{ coin.date_minted }} • {{ coin.reference }}</p>
        </div>
      </a>
    </div>
  {% endfor %}
</div>

<style>
.showcase-intro {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 3rem;
  font-size: 1.1rem;
  color: var(--global-text-color-light);
}

.showcase-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.showcase-item {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
  background: var(--global-card-bg-color);
  border: 1px solid var(--global-divider-color);
  padding: 1rem;
}

.showcase-item:hover {
  transform: scale(1.02);
}

.showcase-item img {
  width: 100%;
  height: auto;
  object-fit: contain;
  display: block;
}

.showcase-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
  color: #ffffff;
  padding: 2rem 1rem 1rem;
  transform: translateY(100%);
  transition: transform 0.3s ease;
}

.showcase-item:hover .showcase-overlay {
  transform: translateY(0);
}

.showcase-overlay h3 {
  margin: 0 0 0.5rem;
  font-size: 1.2rem;
  color: #ffffff !important;
}

.showcase-overlay p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.9;
  color: #ffffff !important;
}

.showcase-item a {
  text-decoration: none;
  color: inherit;
}

@media (max-width: 768px) {
  .showcase-gallery {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
</style>
