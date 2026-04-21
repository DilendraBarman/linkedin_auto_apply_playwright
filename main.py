import yaml
from utils.browser import get_browser
from pages.login_page import login
from pages.search_page import search_jobs
from pages.apply_page import find_easy_apply_jobs, apply_jobs

if __name__ == "__main__":
    with open("config.yaml") as f:
        cfg = yaml.safe_load(f)

    p, browser, context, page = get_browser(headless=False)
    login(page, cfg["login"]["email"], cfg["login"]["password"])
    search_jobs(page, cfg["search"]["keywords"], cfg["search"]["location"])
    links = find_easy_apply_jobs(page, total_pages=cfg["search"]["pages_to_scrape"])
    print(f"Total Easy Apply jobs found: {len(links)}")
    print("Job links:", links)
    apply_jobs(page, links, cfg["resume_path"], cfg["cover_letter_path"], cfg)

    browser.close()
    p.stop()
