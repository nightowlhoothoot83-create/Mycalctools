# Craft fair calculator release

Additive utility for the existing MyCalcTools static Cloudflare Pages site. Reuses its domain and brand; no new domain or paid service. Existing main inspected at 9d323220f2abd86d3bf2cc55034c9fdf61f28fd4 on 2026-11-14. PR #42 was merged before integration; this branch starts from ae8ef95 and preserves its changes. No AGENTS.md exists in the inspected recursive main tree. Only the XML sitemap is additionally updated for discovery. Existing calculators and shared scripts are unchanged.

## Why this task
Exact keyword: **craft fair profit calculator**. Audience: English-speaking independent makers; currency display includes AUD/USD/GBP/EUR/CAD/NZD, without currency conversion. Existing indexed free competing calculators establish a task people build tools around, a weak proxy rather than verified search volume or purchasing demand. Query volume, conversions and expected earnings remain unavailable. See the research evidence report for competitor sources and limitations.

Useful improvement: no-account local multi-event comparisons, separate cash and labour-adjusted profit, break-even on both bases, spreadsheet-safe CSV export and printable results. Input assumptions and formula are explained with an original worked example.

## Checks
Run `node tests/craft-fair-profit.cjs` (7 numerical/validation/CSV test cases). Run `node --check craft-fair-profit.js` and `node --check craft-fair-profit-ui.js`. Browser QA separately covers actual saving/export, invalid input, mobile layout and links. Unit tests do not establish browser or live deployment success.

## Monetisation and limits
The page links to the owner's existing ADGDownloads Etsy shop and discloses the relationship. This verifies neither checkout nor any particular listing availability. No paid upgrade checkout is fabricated. A matching paid maker-event workbook is a possible next offer after actual listing/delivery verification. No affiliate offer is enabled without approval evidence. Advertising is optional and not a launch dependency. No AI calls or server calculations per visitor. Incremental runtime cost should be zero on the existing free Pages plan within current plan limits; account billing and usage must be verified by the owner connection.

Campaign manifest includes platform-specific original copy, original SVG, a short-video storyboard, UTM links, and empty publication confirmation fields. It is preparation, not a published campaign or rendered video. Existing publishing services should rasterise the SVG to a supported image format before scheduling.

## Safe launch and rollback
Deploy via existing Cloudflare Pages source branch after browser acceptance. Check the new URL and both JS assets return expected source. Retain the prior Cloudflare deployment ID for one-step rollback if the site regresses. Since this change is additive, reverting its commit also removes the tool without changing existing calculators. Add homepage and sitemap discovery in a later conflict-free patch after concurrent PR #42 is reconciled; until then direct promotion can use the exact new URL. A new domain is unnecessary, so no availability or purchase claim is made.

## Analytics
Campaign UTM links are ready for host analytics and Etsy referral reports where available. No visitor identifiers or calculator inputs are sent by this utility. No conversion or sale is reported without provider evidence. Local scenario saving is not business income tracking.

## Acceptance completed
Seven numerical/CSV tests and existing integrity validation pass. Headless Chromium checked actual calculation, save/reload persistence, CSV download, zero-sales loss and 390px mobile width without JS errors. Desktop and mobile screenshots were inspected. Cookie consent/shared branding are reused; a page-scoped footer width correction resolves mobile overflow. These local checks do not themselves verify a live deployment.
