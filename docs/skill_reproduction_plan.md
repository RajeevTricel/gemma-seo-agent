# Skill Reproduction Plan

## Goal
Reproduce Claude-style SEO and marketing assistant behaviour using Gemma, LoRA fine-tuning, RAG, and tool-calling.

## Source Blueprints
- claude-seo-1.9.6
- marketingskills-1.9.0

## Architecture
Fine-tuning teaches behaviour and formatting.
RAG stores skill documentation and marketing/SEO frameworks.
Tools fetch live data from PageSpeed, GSC, GA4, SE Ranking, databases, and website crawlers.

## Core Skill Groups
1. SEO audit
2. Technical SEO
3. PageSpeed/Core Web Vitals
4. Google Search Console/GA4 analysis
5. AI SEO/GEO/AEO
6. Schema markup
7. Local SEO
8. Ecommerce/WooCommerce SEO
9. CRO
10. Copywriting/content strategy
11. Paid ads
12. Product marketing context

## First Dataset Target
100 examples:
- 20 SEO audit/technical
- 15 PageSpeed/CWV
- 10 GSC/GA4
- 10 GEO/AEO
- 10 ecommerce/WooCommerce
- 10 CRO
- 10 copy/content
- 5 paid ads
- 5 product marketing context
- 5 missing-data/refusal-to-guess

## Output Style
Every answer should be practical, prioritized, and split into:
- Priority
- What this means
- Why it matters
- Recommended actions
- Developer actions
- Marketing actions
- Business impact
- What to check next