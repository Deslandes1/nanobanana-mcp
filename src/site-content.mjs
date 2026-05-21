import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const DEFAULT_CONTENT_PATH = path.resolve(
  __dirname,
  "../data/site-content.json"
);

const NAMESPACE_RE = /^[a-z][a-z0-9-]*$/u;

const OPTIONAL_URL_FIELDS = [
  "pricingUrl",
  "docsUrl",
  "blogUrl",
  "aboutUrl",
  "faqUrl",
  "communityUrl",
];

function assertAbsoluteUrl(value, fieldName) {
  try {
    const parsed = new URL(value);
    if (!parsed.protocol.startsWith("http")) {
      throw new Error("Only http and https URLs are supported.");
    }
  } catch (error) {
    throw new Error(
      `${fieldName} must be a valid absolute URL. Received "${value}".`,
      { cause: error }
    );
  }
}

function assertUniqueSlugs(pages) {
  const seen = new Set();
  for (const page of pages) {
    if (seen.has(page.slug)) {
      throw new Error(`Duplicate page slug found: "${page.slug}".`);
    }
    seen.add(page.slug);
  }
}

function assertUniqueToolNames(tools) {
  const seen = new Set();
  for (const tool of tools) {
    if (seen.has(tool.name)) {
      throw new Error(`Duplicate tool name found: "${tool.name}".`);
    }
    seen.add(tool.name);
  }
}

export function validateSiteContent(content) {
  if (!content.site.name.trim()) {
    throw new Error("site.name is required.");
  }
  if (!NAMESPACE_RE.test(content.namespace || "")) {
    throw new Error(
      `namespace must be lowercase kebab-case. Received "${content.namespace}".`
    );
  }
  if (content.pages.length === 0) {
    throw new Error("At least one page is required.");
  }
  assertAbsoluteUrl(content.site.websiteUrl, "site.websiteUrl");
  for (const field of OPTIONAL_URL_FIELDS) {
    if (content.site[field] !== undefined) {
      assertAbsoluteUrl(content.site[field], `site.${field}`);
    }
  }
  assertUniqueSlugs(content.pages);
  assertUniqueToolNames(content.tools || []);
  for (const page of content.pages) {
    if (!page.slug.trim()) {
      throw new Error("Each page.slug is required.");
    }
    if (!page.title.trim()) {
      throw new Error(`Page "${page.slug}" is missing title.`);
    }
    if (!page.text.trim()) {
      throw new Error(`Page "${page.slug}" is missing text.`);
    }
  }
  for (const tool of content.tools || []) {
    if (!tool.name.trim()) {
      throw new Error("Each tool.name is required.");
    }
    if (!tool.description.trim()) {
      throw new Error(`Tool "${tool.name}" is missing description.`);
    }
    if (!tool.result?.text?.trim()) {
      throw new Error(`Tool "${tool.name}" is missing result.text.`);
    }
  }
  return content;
}

export function loadSiteContent(contentPath = DEFAULT_CONTENT_PATH) {
  const raw = readFileSync(contentPath, "utf8");
  return validateSiteContent(JSON.parse(raw));
}

export function getPageBySlug(content, slug) {
  return content.pages.find((page) => page.slug === slug);
}
