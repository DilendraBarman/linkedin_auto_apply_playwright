import time

def search_jobs(page, keywords, location):
    page.goto("https://www.linkedin.com/jobs")
    job_input = page.wait_for_selector("input[placeholder*='Describe the job you want']")
    job_input.fill("")
    job_input.fill(keywords)
    # page.fill("input[placeholder*='Describe the job you want']", keywords)
    job_input.press("Enter")
    page.wait_for_timeout(500)

    # page.fill("input[aria-label='City, state, or zip code']", location)
    # page.click("button[aria-label='Search']")
    # page.wait_for_selector(".jobs-search-results__list-item")
    # print(f"🔍 Searching jobs for '{keywords}' in '{location}'...")

    # Optional: apply Easy Apply filter
    try:
        page.locator("button[aria-label='Easy Apply filter.']").click()
        time.sleep(1)
        print("✅ Applied Easy Apply filter.")
    except:
        print("⚠️ Easy Apply filter not found (may vary by region)")

