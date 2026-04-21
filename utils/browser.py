from playwright.sync_api import sync_playwright

def get_browser(headless=False):
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=headless, slow_mo=50)
    context = browser.new_context()
    page = context.new_page()
    return p, browser, context, page
