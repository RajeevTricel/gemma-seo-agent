# PageSpeed Priority Guide

## Purpose

Use this when deciding whether PageSpeed, Core Web Vitals, LCP, INP, CLS, JavaScript, CSS, images, caching, or third-party scripts should be prioritised.

## Important principle

A low PageSpeed score is not automatically the highest priority. Prioritise speed fixes by business impact, affected page type, mobile traffic, organic visibility, conversion path, and effort.

## High priority PageSpeed issues

Treat as High when:
- slow pages are revenue or lead-generation pages
- mobile users are important
- LCP/INP/CLS are poor on important organic landing pages
- slow templates affect many important pages
- Core Web Vitals issues overlap with ranking or conversion drops
- third-party scripts block key interactions
- hero/LCP assets are oversized above the fold

## Medium priority PageSpeed issues

Treat as Medium when:
- conversions are stable or improving
- issue affects useful but lower-value pages
- the fix is moderate effort
- evidence is incomplete
- speed is poor but organic visibility is stable

## Low priority PageSpeed issues

Treat as Low when:
- issue affects low-traffic blog pages only
- conversion paths are not affected
- fix effort is high and expected benefit is low
- PageSpeed lab score is low but field data/user impact is not proven

## Common fixes

LCP:
- compress/resize hero images
- use WebP/AVIF
- preload confirmed LCP image
- do not lazy-load above-the-fold LCP image
- improve server response time

INP:
- reduce main-thread JavaScript
- delay non-critical scripts
- remove unused plugins
- improve interaction handlers

CLS:
- set image/video dimensions
- reserve space for banners/forms
- avoid late-loading layout shifts
- stabilise fonts and embeds

Caching/CDN:
- cache static assets
- use CDN for images/scripts/CSS
- set long cache TTL for versioned assets

## PageSpeed vs conversions

If PageSpeed is low but conversions are up:
- do not remove conversion elements blindly
- check affected URLs and device split
- compare GA4 conversions with GSC landing-page data
- prioritise high-value pages first
- test changes carefully so conversion gains are not broken

## Evidence needed

Ask for:
- affected URLs
- PageSpeed or CrUX data
- LCP, INP, CLS
- device split
- organic landing-page data
- conversions by page/device
- recent site changes
- plugin/script changes