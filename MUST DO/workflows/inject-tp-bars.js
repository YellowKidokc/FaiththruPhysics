/**
 * Batch inject tp-inject.js and generate per-page article-meta.
 *
 * Usage:
 *   node inject-tp-bars.js [directory] [--dry-run]
 *
 * Example:
 *   node inject-tp-bars.js moral-decline
 *   node inject-tp-bars.js moral-decline --dry-run
 */
const fs = require('fs');
const path = require('path');

const targetDir = process.argv[2] || '.';
const dryRun = process.argv.includes('--dry-run');

const SKIP_DIRS = ['archive', 'backup', '_built', 'codex_build', 'work', 'production-vault', 'node_modules'];

const SHELL_PATTERNS = [
  /site-shell\.js/,
  /tp-inject\.js/,
  /tp-pill-player\.js/,
  /tp-pill-player\.css/,
  /class=["']site-nav-bar["']/,
  /<div[^>]*class=["'][^"']*ftp-topbar/,
  /<div[^>]*class=["'][^"']*tp-top-bar/,
  /<div[^>]*class=["'][^"']*tp-bottom-bar/,
  /<div[^>]*class=["'][^"']*mda-topbar/,
  /<div[^>]*class=["'][^"']*tp-player-block/,
  /<div[^>]*class=["'][^"']*tp-pill-bar/,
  /<div[^>]*class=["'][^"']*tp-read-aloud/
];

// MDA nine-domain classification mapping.
const DOMAIN_MAP = {
  F: { tag: 'Family', color: '#378ADD' },
  T: { tag: 'Trust', color: '#D85A30' },
  S: { tag: 'Safety', color: '#1D9E75' },
  C: { tag: 'Self-Control', color: '#7F77DD' },
  M: { tag: 'Mental Health', color: '#D4537E' },
  E: { tag: 'Economic', color: '#f59e0b' },
  P: { tag: 'Civic', color: '#3bb39a' },
  'Σ': { tag: 'Shared Meaning', color: '#d4af37' },
  I: { tag: 'Intergenerational', color: '#5b9bd5' }
};

function shouldSkipDir(dirName) {
  const lower = dirName.toLowerCase();
  return SKIP_DIRS.some((skip) => lower.includes(skip));
}

function hasExistingShell(html) {
  return SHELL_PATTERNS.some((pattern) => pattern.test(html));
}

function parsePageMeta(html) {
  const match = html.match(/<!--\s*PAGE_META\s*([\s\S]*?)-->/);
  if (!match) return null;
  const meta = {};
  match[1].split('\n').forEach((line) => {
    const kv = line.match(/^\s*(\w+):\s*(.*?)\s*$/);
    if (kv) meta[kv[1]] = kv[2];
  });
  return meta;
}

function buildClassification(domainsStr, primaryDomain) {
  if (!domainsStr) return [{ tag: 'theophysics', pct: 100, color: '#d4af37' }];

  const letters = domainsStr.split(/[,\s]+/).filter(Boolean);
  const unique = [...new Set(letters)];
  const mapped = unique.map((letter) => DOMAIN_MAP[letter] || { tag: letter, color: '#d4af37' });

  let weights = mapped.map((item) => ({ ...item, weight: 1 }));
  if (primaryDomain) {
    weights = weights.map((item) =>
      item.tag === (DOMAIN_MAP[primaryDomain]?.tag || primaryDomain)
        ? { ...item, weight: 2 }
        : item
    );
  }

  const totalWeight = weights.reduce((sum, item) => sum + item.weight, 0);
  let percentages = weights.map((item) => ({
    tag: item.tag,
    color: item.color,
    raw: (item.weight / totalWeight) * 100
  }));

  percentages = percentages.map((item) => ({ ...item, pct: Math.round(item.raw / 5) * 5 }));
  let sum = percentages.reduce((s, item) => s + item.pct, 0);
  if (sum !== 100 && percentages.length > 0) {
    const diff = 100 - sum;
    const maxIndex = percentages.reduce((maxIdx, item, idx, arr) =>
      item.pct > arr[maxIdx].pct ? idx : maxIdx, 0);
    percentages[maxIndex].pct += diff;
  }
  percentages = percentages.filter((item) => item.pct > 0);

  return percentages.map(({ tag, color, pct }) => ({ tag, pct, color }));
}

function buildMeta(html, filePath) {
  const pageMeta = parsePageMeta(html);
  const slug = pageMeta?.article || path.basename(filePath, path.extname(filePath));
  const title = pageMeta?.title || extractTitle(html) || slug;
  const series = pageMeta?.series || inferSeries(filePath);
  const classification = buildClassification(pageMeta?.domains, pageMeta?.primary_domain);

  return {
    slug,
    title,
    series,
    classification,
    reading_levels: ['story', 'plain'],
    audio_api: 'https://faith-audio-pipeline.davidokc28.workers.dev/api/audio'
  };
}

function extractTitle(html) {
  const match = html.match(/<title[^>]*>([^<]+)<\/title>/i);
  return match ? match[1].split('|')[0].trim() : null;
}

function inferSeries(filePath) {
  const parts = filePath.split(path.sep);
  if (parts.includes('moral-decline')) return 'moral-decline';
  if (parts.includes('mda')) return 'mda';
  if (parts.includes('genesis-to-quantum')) return 'genesis-to-quantum';
  if (parts.includes('one-page-stories')) return 'one-page-stories';
  if (parts.includes('isomorphism')) return 'isomorphism';
  if (parts.includes('convergence-series')) return 'convergence-series';
  if (parts.includes('convergence-deep')) return 'convergence-deep';
  if (parts.includes('master-equation')) return 'master-equation';
  if (parts.includes('consciousness')) return 'consciousness';
  return 'faith-through-physics';
}

function injectScript(html) {
  const scriptTag = '<script src="/components/tp-inject.js" data-theme="dark"></script>\n';
  if (/<\/body>/i.test(html)) {
    return html.replace(/<\/body>/i, (match) => scriptTag + match);
  }
  if (/<\/html>/i.test(html)) {
    return html.replace(/<\/html>/i, (match) => scriptTag + match);
  }
  return html + '\n' + scriptTag;
}

function injectMeta(html, meta) {
  if (html.includes('id="article-meta"')) return html;
  const metaBlock = `<script id="article-meta" type="application/json">\n${JSON.stringify(meta, null, 2)}\n</script>\n`;
  if (/<\/head>/i.test(html)) {
    return html.replace(/<\/head>/i, (match) => metaBlock + match);
  }
  if (/<head[^>]*>/i.test(html)) {
    return html.replace(/<head[^>]*>/i, (match) => match + '\n' + metaBlock);
  }
  if (/<body[^>]*>/i.test(html)) {
    return html.replace(/<body[^>]*>/i, (match) => metaBlock + match);
  }
  return metaBlock + html;
}

function processFile(filePath) {
  let html = fs.readFileSync(filePath, 'utf8');

  if (hasExistingShell(html)) {
    return { action: 'skipped-existing-shell', path: filePath };
  }

  const meta = buildMeta(html, filePath);
  let metaInjected = false;
  let scriptInjected = false;

  if (!html.includes('id="article-meta"')) {
    if (!dryRun) {
      html = injectMeta(html, meta);
      fs.writeFileSync(filePath, html, 'utf8');
    }
    metaInjected = true;
  }

  if (!/tp-inject\.js/.test(html)) {
    if (!dryRun) {
      html = injectScript(html);
      fs.writeFileSync(filePath, html, 'utf8');
    }
    scriptInjected = true;
  }

  if (metaInjected || scriptInjected) {
    return { action: 'injected', path: filePath, metaInjected, scriptInjected };
  }

  return { action: 'skipped-no-action', path: filePath };
}

function walk(dir, results = []) {
  for (const entry of fs.readdirSync(dir)) {
    const fullPath = path.join(dir, entry);
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      if (!shouldSkipDir(entry)) walk(fullPath, results);
    } else if (stat.isFile() && /\.html?$/i.test(entry)) {
      results.push(fullPath);
    }
  }
  return results;
}

const files = walk(targetDir);
const results = files.map(processFile);

const summary = {
  total: files.length,
  injected: results.filter((r) => r.action === 'injected').length,
  skippedExistingShell: results.filter((r) => r.action === 'skipped-existing-shell').length,
  skippedNoAction: results.filter((r) => r.action === 'skipped-no-action').length
};

console.log(JSON.stringify(summary, null, 2));
if (dryRun) {
  console.log('\nDry run results (first 10):');
  results.slice(0, 10).forEach((r) => console.log(r.action, r.path));
}
