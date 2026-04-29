# GSC and GA4 Diagnosis Guide

## Purpose

Use this when diagnosing organic traffic, ranking, CTR, impression, landing-page, and conversion changes.

## GSC interpretation patterns

Clicks down, impressions stable, position stable:
- likely CTR issue
- check titles/meta, SERP features, competitor snippets, query mix, brand/non-brand split

Clicks down, impressions down, position stable:
- possible demand drop, seasonality, query volume change, or reduced search interest

Clicks down, position down:
- likely ranking loss
- compare affected queries/pages
- check technical changes, content changes, competitors, internal links, canonicals, indexation

Impressions up, clicks down:
- likely broader visibility with weaker CTR or lower-intent queries
- check query mix and page intent match

CTR down, position stable:
- likely snippet/SERP issue
- check title tags, meta descriptions, rich results, competitors, SERP features

Organic sessions down, conversions stable:
- may indicate low-intent traffic dropped but valuable traffic remained
- check landing-page split and conversion rate

Organic sessions up, leads down:
- likely traffic quality or conversion issue
- check landing pages, forms, CTAs, device split, intent mismatch

## GA4 interpretation

Use GA4 to check:
- organic sessions
- landing pages
- conversions
- engagement rate
- device category
- form submissions
- phone/email clicks
- assisted conversion paths
- page-level conversion rate

## Missing data rules

Do not claim exact causes without:
- date range
- affected pages
- affected queries
- GSC clicks/impressions/CTR/position
- GA4 organic sessions/conversions
- recent site changes
- indexation/crawl checks

## Branded vs non-branded

Always separate branded and non-branded queries where possible:
- branded drop may indicate demand/reputation issue
- non-branded drop may indicate SEO/ranking/content issue

## First checks for ranking drop

1. Confirm date range.
2. Compare GSC pages and queries before vs after.
3. Split by device and country.
4. Check whether position, CTR, or impressions changed most.
5. Check affected landing pages in GA4.
6. Check recent technical/content changes.
7. Inspect priority URLs for indexation/canonical issues.