import { loadSiteContent } from "./site-content.mjs";
import { startSiteServer } from "./server.mjs";

async function main() {
  const content = loadSiteContent();
  await startSiteServer(content);
}

main().catch((error) => {
  console.error("Failed to start minimal-site-mcp.");
  console.error(error);
  process.exitCode = 1;
});
