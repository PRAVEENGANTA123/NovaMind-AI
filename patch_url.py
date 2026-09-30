import os

path = os.path.join("services", "ai", "url_service.py")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update timeouts & page budgets for fast discovery
content = content.replace("DEFAULT_TIMEOUT = 12", "DEFAULT_TIMEOUT = 5")
content = content.replace("DEFAULT_CRAWL_TIMEOUT = 90", "DEFAULT_CRAWL_TIMEOUT = 10")
content = content.replace("AUTO_MAX_PAGES_NO_QUERY = 80", "AUTO_MAX_PAGES_NO_QUERY = 1")
content = content.replace("AUTO_MAX_PAGES_QUERY = 15", "AUTO_MAX_PAGES_QUERY = 5")

# 2. Target replacement block
target = "                for link in internal:\n                    enqueue(link, \"internal-link\")"

replacement = """                for link in internal:
                    enqueue(link, "internal-link")

                # Fast Mode: Register all homepage navigation links instantly
                if not query and source == "root":
                    for link in internal:
                        if cls.is_same_domain(link, root_domain):
                            path_slug = urlparse(link).path.strip("/").replace("-", " ").replace("_", " ").replace("/", " - ")
                            clean_title = path_slug.title() if path_slug else "Main Portal / Section"
                            cat = cls.classify_resource(link, clean_title)
                            resources.append(WebsiteResource(
                                url=link,
                                title=clean_title,
                                category=cat,
                                resource_type="HTML",
                                source="homepage-menu",
                                status_code=200
                            ))
                    break"""

if target in content and "# Fast Mode:" not in content:
    content = content.replace(target, replacement)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ services/ai/url_service.py successfully patched for fast discovery!")
elif "# Fast Mode:" in content:
    print("ℹ️ File is already patched.")
else:
    print("⚠️ Target block not found. Checking if file structure changed.")
