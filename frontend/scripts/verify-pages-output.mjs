import { access, readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const frontendRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outputRoot = path.resolve(frontendRoot, "../src/typhoon_vn/dashboard");
const indexPath = path.join(outputRoot, "index.html");
const indexHtml = await readFile(indexPath, "utf8");
const assetPaths = [...indexHtml.matchAll(/(?:src|href)="\/(assets\/[^"?]+)"/g)].map(
    (match) => match[1],
);

if (assetPaths.length === 0) {
    throw new Error(`No production assets referenced by ${indexPath}`);
}

await Promise.all(assetPaths.map((assetPath) => access(path.join(outputRoot, assetPath))));

const javascript = await Promise.all(
    assetPaths
        .filter((assetPath) => assetPath.endsWith(".js"))
        .map((assetPath) => readFile(path.join(outputRoot, assetPath), "utf8")),
);
const bundleText = javascript.join("\n");

for (const requiredMarker of ["OLLAMA CLOUD", "/api/ai/chat"]) {
    if (!bundleText.includes(requiredMarker)) {
        throw new Error(`Pages output is stale: missing ${requiredMarker}`);
    }
}

console.log(`Verified Pages output: ${assetPaths.length} assets and Ollama UI markers present.`);
