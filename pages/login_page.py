import time

def login(page, email, password):
    page.goto("https://www.linkedin.com/login")
    page.fill("#username", email)
    page.fill("#password", password)
    page.click("button[type='submit']")
    page.wait_for_url("https://www.linkedin.com/feed/", timeout=10000)
    print("✅ Logged in to LinkedIn")
    time.sleep(2)
