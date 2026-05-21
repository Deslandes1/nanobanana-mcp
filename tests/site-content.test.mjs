import test from "node:test";
import assert from "node:assert/strict";

import {
  DEFAULT_CONTENT_PATH,
  loadSiteContent,
  validateSiteContent,
} from "../src/site-content.mjs";

function minimalContent() {
  return {
    site: {
      name: "Example",
      tagline: "Example",
      websiteUrl: "https://example.com",
      supportEmail: "hello@example.com",
    },
    namespace: "example",
    pages: [
      {
        slug: "overview",
        title: "Overview",
        description: "Overview page",
        mimeType: "text/markdown",
        text: "# One",
      },
    ],
    tools: [
      {
        name: "get_site_overview",
        description: "Returns the site overview.",
        result: { mimeType: "text/markdown", text: "# Overview" },
      },
    ],
  };
}

test("default content loads with required metadata", () => {
  const content = loadSiteContent(DEFAULT_CONTENT_PATH);
  assert.ok(content.site.websiteUrl.startsWith("https://"));
  assert.ok(content.pages.length >= 1);
  assert.ok(content.tools.length >= 1);
  assert.ok(/^[a-z][a-z0-9-]*$/u.test(content.namespace));
});

test("validateSiteContent rejects duplicate slugs", () => {
  const content = minimalContent();
  content.pages.push({
    slug: "overview",
    title: "Overview Two",
    description: "Duplicate slug",
    mimeType: "text/markdown",
    text: "# Two",
  });
  assert.throws(() => validateSiteContent(content), /Duplicate page slug/);
});

test("validateSiteContent rejects duplicate tool names", () => {
  const content = minimalContent();
  content.tools.push({
    name: "get_site_overview",
    description: "duplicate",
    result: { mimeType: "text/plain", text: "x" },
  });
  assert.throws(() => validateSiteContent(content), /Duplicate tool name/);
});

test("validateSiteContent rejects invalid namespace", () => {
  const content = minimalContent();
  content.namespace = "Bad_Name";
  assert.throws(() => validateSiteContent(content), /namespace must be lowercase/);
});
