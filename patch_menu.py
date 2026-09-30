import os
import re

path = os.path.join("services", "ai", "url_service.py")

with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# Make sure DEFAULT_TIMEOUT is fast
code = re.sub(r"DEFAULT_TIMEOUT\s*=\s*\d+", "DEFAULT_TIMEOUT = 5", code)
code = re.sub(r"DEFAULT_CRAWL_TIMEOUT\s*=\s*\d+", "DEFAULT_CRAWL_TIMEOUT = 10", code)

# Ensure the discovery loop extracts all sub-links from root response
old_block_pattern = r"(resource,\s*internal,\s*external\s*=\s*cls\._extract_content\(.*?\)\s*resources\.append\(resource\))"

new_block = """resource, internal, external = cls._extract_content(current_url, response, source)
                resources.append(resource)

                # Direct Root Menu Extraction: Register all intra-domain links immediately
                if not query and source == "root":
                    seen_links = {cls.normalize_url(resource.url)}
                    for link in internal:
                        norm = cls.normalize_url(link)
                        if norm and cls.is_same_domain(norm, root_domain) and norm not in seen_links:
                            seen_links.add(norm)
                            path_slug = urlparse(norm).path.strip("/").replace("-", " ").replace("_", " ").replace("/", " - ")
                            clean_title = path_slug.title() if path_slug else "Main Portal / Section"
                            cat = cls.classify_resource(norm, clean_title)
                            resources.append(WebsiteResource(
                                url=norm,
                                title=clean_title,
                                category=cat,
                                resource_type="HTML",
                                source="homepage-menu",
                                status_code=200
                            ))
                    print(f"[WebsiteDiscovery] Extracted {len(resources)} sub-links directly from homepage menu.")
                    break"""

if "Direct Root Menu Extraction" not in code:
    code = re.sub(old_block_pattern, new_block, code, count=1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ Successfully patched url_service.py for deep menu link extraction!")
else:
    print("ℹ️ File already contains direct root menu extraction.")
