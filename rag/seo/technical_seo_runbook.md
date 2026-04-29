# Technical SEO Runbook

## Purpose

Use this document when diagnosing technical SEO, crawlability, indexation, sitemap, canonical, redirect, robots, and template issues.

## Priority rules

Critical issues:
- Important revenue or lead-generation pages are accidentally noindex.
- Important pages are blocked in robots.txt.
- Canonical tags point important pages to the wrong URL.
- Migration errors cause important URLs to redirect incorrectly, 404, or disappear.
- Sitemap contains the wrong canonical/indexable URLs during a migration.

High priority issues:
- Important category, product, service, or landing pages have crawl/indexation problems.
- Internal links to priority pages are broken.
- Redirect chains affect important pages.
- JavaScript hides important content from crawlers.
- Duplicate/cannibalised pages compete for the same search intent.

Medium priority issues:
- Duplicate titles or meta descriptions on lower-value pages.
- Sitemap includes redirected/noindex/non-canonical URLs.
- Weak internal linking to informational pages.
- Minor canonical inconsistencies on non-critical URLs.

Low priority issues:
- Small metadata polish.
- Minor alt text gaps.
- Cosmetic HTML issues that do not affect crawlability, indexation, UX, or conversions.

## Noindex diagnosis

If important pages are noindex:
1. Confirm whether the noindex is intentional.
2. Identify page type and business value.
3. Check current traffic, impressions, clicks, conversions, backlinks, and internal links.
4. Check whether the page is canonical, 200-status, crawlable, and included in the sitemap.
5. Remove noindex only from pages that should rank.
6. Keep noindex on duplicate, thin, internal search, filtered, staging, or low-value pages.

## Robots.txt diagnosis

Robots.txt should not block important pages, CSS, JavaScript, images, or resources needed for rendering.

Check:
- Disallow rules.
- Important product/service/category paths.
- Sitemap declaration.
- Whether blocked URLs are still indexed from external links.
- Whether crawl blocking is being confused with noindex.

## Sitemap rules

A clean XML sitemap should include only:
- 200-status URLs.
- Canonical URLs.
- Indexable URLs.
- Pages that should appear in search.

Remove:
- Redirected URLs.
- 404/5xx URLs.
- Noindex URLs.
- Canonicalised duplicates.
- Parameter/filter URLs unless intentionally indexable.

## Canonical rules

Canonical tags should:
- Point to the preferred indexable version.
- Be self-referencing on unique pages.
- Not point revenue pages to unrelated pages.
- Not be used to hide serious duplication without fixing internal links.

## Redirect rules

Use 301 redirects for permanent moves.

Check:
- Redirect chains.
- Redirect loops.
- Redirects to irrelevant pages.
- Lost internal links after migration.
- Important old URLs without suitable destinations.

## Default response approach

When evidence is missing, do not guess. Ask for:
- affected URLs
- crawl export
- GSC indexation data
- sitemap URL
- robots.txt
- canonical tags
- status codes
- recent release/migration history