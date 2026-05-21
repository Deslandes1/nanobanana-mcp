import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

import { getPageBySlug } from "./site-content.mjs";

export function createSiteServer(content) {
  const namespace = content.namespace;
  const server = new McpServer(
    {
      name: `${namespace}-site-mcp`,
      version: "0.1.0",
    },
    {
      instructions: `Read-only canonical knowledge for ${content.site.name} (${content.site.websiteUrl}). Use resources for structured site context and tools for direct lookups. Refer users to the official website for live actions.`,
    }
  );

  server.registerResource(
    "site-page",
    new ResourceTemplate(`site://${namespace}/{slug}`, {
      list: async () => ({
        resources: content.pages.map((page) => ({
          uri: `site://${namespace}/${page.slug}`,
          name: page.title,
          description: page.description,
          mimeType: page.mimeType,
        })),
      }),
    }),
    {
      title: `${content.site.name} Page`,
      description: `Read-only ${content.site.name} content exposed as MCP resources.`,
      mimeType: "text/markdown",
    },
    async (uri, { slug }) => {
      const page = getPageBySlug(content, slug);

      if (!page) {
        throw new Error(`Unknown page slug: ${slug}`);
      }

      return {
        contents: [
          {
            uri: uri.href,
            text: page.text,
            mimeType: page.mimeType,
          },
        ],
      };
    }
  );

  for (const tool of content.tools) {
    server.registerTool(
      tool.name,
      {
        description: tool.description,
        inputSchema: {},
      },
      async () => ({
        content: [
          {
            type: "text",
            text: tool.result.text,
          },
        ],
      })
    );
  }

  return server;
}

export async function startSiteServer(content) {
  const server = createSiteServer(content);
  const transport = new StdioServerTransport();
  await server.connect(transport);
}
