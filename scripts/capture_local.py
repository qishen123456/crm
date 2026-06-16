#!/usr/bin/env python3
"""Capture local ANGEL CRM screenshots for visual regression comparison."""
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:5175"
OUTPUT_DIR = Path("output/screenshots")
EMAIL = "admin@angel.cn"
PASSWORD = "demo2026"
VIEWPORT = {"width": 1440, "height": 900}

TARGETS = [
    ("login", "/login"),
    ("today", "/app/today"),
    ("dashboard", "/app/dashboard"),
    ("workqueue", "/app/workqueue"),
    ("accounts", "/app/accounts"),
    ("account_detail", "/app/account/a1"),
    ("orders", "/app/orders"),
    ("contacts", "/app/contacts"),
    ("contracts", "/app/contracts"),
    ("payments", "/app/payments"),
    ("products", "/app/products"),
    ("settings", "/app/settings"),
    ("pipeline", "/app/pipeline"),
    ("campaigns", "/app/campaigns"),
    ("leads", "/app/leads"),
    ("pool", "/app/pool"),
    ("end_users", "/app/end-users"),
    ("team", "/app/team"),
    ("country_reports", "/app/country-reports"),
    ("executive_report", "/app/report"),
    ("retail", "/app/retail"),
    ("project_updates", "/app/project-updates"),
    ("import", "/app/import"),
    ("invite", "/app/invite"),
    ("attendance", "/app/attendance"),
    ("log_activity", "/app/log-activity"),
    ("invoices", "/app/invoices"),
]


def login(page):
    page.goto(f"{BASE_URL}/login")
    page.wait_for_selector(".angel-login-form", timeout=10000)
    page.get_by_label("工作邮箱").fill(EMAIL)
    page.get_by_label("密码").fill(PASSWORD)
    page.locator(".angel-login-submit").click()
    page.wait_for_url(lambda url: "/app/" in url, timeout=10000)
    page.wait_for_timeout(800)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport=VIEWPORT)
        page = context.new_page()

        # Login first so session cookie is shared
        login(page)

        for name, route in TARGETS:
            url = f"{BASE_URL}{route}"
            page.goto(url)
            page.wait_for_load_state("networkidle", timeout=15000)
            page.wait_for_timeout(1200)
            out = OUTPUT_DIR / f"{name}.png"
            page.screenshot(path=str(out), full_page=False)
            print(f"saved {out} ({page.viewport_size['width']}x{page.viewport_size['height']})")

        browser.close()


if __name__ == "__main__":
    main()
