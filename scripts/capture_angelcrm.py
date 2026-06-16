import argparse
import hashlib
import json
import mimetypes
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urlparse

from playwright.sync_api import BrowserContext, Error, Page, Request, Response, sync_playwright


BASE_URL = "https://angelcrm.netlify.app"
LOGIN_URL = f"{BASE_URL}/login"
EMAIL = "admin@angel.cn"
PASSWORD = "demo2026"

OUTPUT_DIR = Path("output")
ASSETS_DIR = OUTPUT_DIR / "assets"
BUNDLES_DIR = OUTPUT_DIR / "bundles"
DOM_DIR = OUTPUT_DIR / "dom"
API_DIR = OUTPUT_DIR / "api"
ROUTES_DIR = OUTPUT_DIR / "routes"
DESKTOP_DIR = OUTPUT_DIR / "desktop"
MOBILE_DIR = OUTPUT_DIR / "mobile"
METADATA_DIR = OUTPUT_DIR / "metadata"

PAGE_WAIT_MS = 1200
DOWNLOADABLE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".svg",
    ".gif",
    ".webp",
    ".ico",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".js",
    ".css",
}

NAV_TARGETS: List[Tuple[str, str, str]] = [
    ("01_today", "Today", "/app/today"),
    ("02_dashboard", "Dashboard", "/app/dashboard"),
    ("03_work_queue", "Work Queue", "/app/workqueue"),
    ("04_attendance", "Attendance", "/app/attendance"),
    ("05_campaigns", "Campaigns", "/app/campaigns"),
    ("06_leads", "Leads", "/app/leads"),
    ("07_retail", "Retail", "/app/retail"),
    ("08_accounts", "Accounts", "/app/accounts"),
    ("10_pool", "Pool", "/app/pool"),
    ("11_contacts", "Contacts", "/app/contacts"),
    ("12_end_users", "End Users", "/app/end-users"),
    ("13_pipeline", "Pipeline", "/app/pipeline"),
    ("14_log_activity", "Log Activity", "/app/log-activity"),
    ("15_project_updates", "Project Updates", "/app/project-updates"),
    ("17_contracts", "Contracts", "/app/contracts"),
    ("18_orders", "Orders", "/app/orders"),
    ("19_invoices", "Invoices", "/app/invoices"),
    ("20_payments", "Payments", "/app/payments"),
    ("21_products", "Products", "/app/products"),
    ("22_country_reports", "Country Reports", "/app/country-reports"),
    ("23_executive_report", "Executive Report", "/app/report"),
    ("24_team", "Team", "/app/team"),
    ("25_settings", "Settings", "/app/settings"),
]


@dataclass
class PageArtifact:
    device: str
    module: str
    label: str
    route: str
    url: str
    title: str
    viewport: str
    full: str
    html: str
    text: str


def ensure_directories() -> None:
    for path in [
        OUTPUT_DIR,
        ASSETS_DIR,
        BUNDLES_DIR,
        DOM_DIR,
        API_DIR,
        ROUTES_DIR,
        DESKTOP_DIR,
        MOBILE_DIR,
        METADATA_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def sanitize_filename(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "_", value.strip())
    return value.strip("_") or "artifact"


def normalize_route(route: str) -> str:
    if route.startswith("http://") or route.startswith("https://"):
        return route
    if route.startswith("/"):
        return f"{BASE_URL}{route}"
    return f"{BASE_URL}/{route}"


def guess_extension(url: str, content_type: Optional[str]) -> str:
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix in DOWNLOADABLE_EXTENSIONS:
        return suffix
    if content_type:
        extension = mimetypes.guess_extension(content_type.split(";")[0].strip())
        if extension:
            return extension
    return ".bin"


def is_first_party(url: str) -> bool:
    host = urlparse(url).netloc
    return not host or "netlify.app" in host


def choose_download_dir(content_type: Optional[str], url: str) -> Optional[Path]:
    if not is_first_party(url):
        return None
    if content_type:
        if content_type.startswith("image/") or content_type.startswith("font/"):
            return ASSETS_DIR
        if "javascript" in content_type or content_type == "text/css":
            return BUNDLES_DIR
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix in {".js", ".css"}:
        return BUNDLES_DIR
    if suffix in {".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp", ".ico", ".woff", ".woff2", ".ttf", ".otf"}:
        return ASSETS_DIR
    return None


def wait_for_page_settle(page: Page, extra_ms: int = PAGE_WAIT_MS) -> None:
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except Error:
        pass
    page.wait_for_timeout(extra_ms)


def scroll_for_lazy_load(page: Page) -> None:
    page.evaluate(
        """
        async () => {
          const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
          window.scrollTo({ top: 0, behavior: 'instant' });
          await delay(300);
          window.scrollTo({ top: document.body.scrollHeight, behavior: 'instant' });
          await delay(700);
          window.scrollTo({ top: 0, behavior: 'instant' });
        }
        """
    )
    page.wait_for_timeout(500)


def try_click(page: Page, selectors: List[str]) -> bool:
    for selector in selectors:
        locator = page.locator(selector).first
        try:
            if locator.count() and locator.is_visible():
                locator.click(timeout=5000)
                page.wait_for_timeout(800)
                return True
        except Error:
            continue
    return False


def click_last_visible_button(page: Page) -> bool:
    buttons = page.locator("button")
    for index in range(buttons.count() - 1, -1, -1):
        try:
            candidate = buttons.nth(index)
            if candidate.is_visible():
                candidate.click(timeout=4000)
                page.wait_for_timeout(1000)
                return True
        except Error:
            continue
    return False


def dismiss_welcome_modal(page: Page) -> None:
    selectors = [
        "button:has-text('Skip')",
        "button:has-text('跳过')",
        ".ant-modal button:has-text('跳过')",
        ".ant-modal-close",
        "[aria-label='Close']",
    ]
    try_click(page, selectors)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)


def login(page: Page) -> None:
    try:
        page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=60000)
    except Error:
        page.goto(LOGIN_URL, wait_until="commit", timeout=60000)
    wait_for_page_settle(page)

    email_selectors = [
        "input[autocomplete='email']",
        "input[type='email']",
        "input[name='email']",
        "input[placeholder*='mail' i]",
        ".ant-input-affix-wrapper input[type='text']",
    ]
    password_selectors = [
        "input[autocomplete='current-password']",
        "input[type='password']",
        "input[name='password']",
    ]

    for selector in email_selectors:
        locator = page.locator(selector).first
        if locator.count():
            locator.fill(EMAIL)
            break

    for selector in password_selectors:
        locator = page.locator(selector).first
        if locator.count():
            locator.fill(PASSWORD)
            break

    clicked = try_click(
        page,
        [
            "button[type='submit']",
            "button.ant-btn-primary",
            "button:has-text('Login')",
            "button:has-text('Sign in')",
            "main button",
        ],
    )
    if not clicked:
        clicked = click_last_visible_button(page)
    if not clicked:
        raise RuntimeError("Could not locate the login button")

    wait_for_page_settle(page, 1800)
    if "/login" in page.url:
        raise RuntimeError(f"Login appears unsuccessful, still on {page.url}")
    dismiss_welcome_modal(page)


def click_text_candidate(page: Page, texts: List[str], scope_selector: Optional[str] = None) -> bool:
    base = page.locator(scope_selector) if scope_selector else page
    for text in texts:
        locator = base.get_by_text(text, exact=False).first
        try:
            if locator.count() and locator.is_visible():
                locator.click(timeout=4000)
                page.wait_for_timeout(1200)
                return True
        except Error:
            continue
    return False


def click_button_by_fragments(page: Page, fragments: List[str], scope_selector: Optional[str] = None) -> bool:
    locator = page.locator(f"{scope_selector} button" if scope_selector else "button")
    for index in range(locator.count()):
        try:
            candidate = locator.nth(index)
            if not candidate.is_visible():
                continue
            text = (candidate.inner_text() or "").strip().replace("\n", " ")
            if any(fragment.lower() in text.lower() for fragment in fragments):
                candidate.click(timeout=4000)
                page.wait_for_timeout(1200)
                return True
        except Error:
            continue
    return False


def click_first_data_row(page: Page) -> bool:
    for index in [2, 1]:
        row = page.locator("tr").nth(index)
        try:
            if row.count() and row.is_visible():
                row.click(timeout=4000)
                page.wait_for_timeout(1200)
                return True
        except Error:
            continue
    return False


def close_overlay_if_present(page: Page) -> None:
    try_click(
        page,
        [
            ".ant-modal-close",
            ".ant-drawer-close",
            "[aria-label='Close']",
            "button:has-text('Close')",
            "button:has-text('取消')",
            "button:has-text('关闭')",
        ],
    )
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)


def save_dom_snapshot(page: Page, slug: str, device_name: str) -> Tuple[str, str]:
    suffix = "_mobile" if device_name == "mobile" else ""
    html_path = DOM_DIR / f"{slug}{suffix}.html"
    text_path = DOM_DIR / f"{slug}{suffix}.txt"
    html_path.write_text(page.content(), encoding="utf-8")
    try:
        text_content = page.locator("body").inner_text(timeout=5000)
    except Error:
        text_content = ""
    text_path.write_text(text_content, encoding="utf-8")
    return str(html_path.as_posix()), str(text_path.as_posix())


def capture_page(page: Page, output_dir: Path, slug: str, device_name: str) -> Dict[str, str]:
    scroll_for_lazy_load(page)
    wait_for_page_settle(page)
    suffix = "_mobile" if device_name == "mobile" else ""
    viewport_path = output_dir / f"{slug}{suffix}_viewport.png"
    full_path = output_dir / f"{slug}{suffix}_full.png"
    page.screenshot(path=str(viewport_path), full_page=False)
    page.screenshot(path=str(full_path), full_page=True)
    html_path, text_path = save_dom_snapshot(page, slug, device_name)
    return {
        "viewport": str(viewport_path.as_posix()),
        "full": str(full_path.as_posix()),
        "html": html_path,
        "text": text_path,
        "url": page.url,
        "title": page.title(),
    }


def discover_navigation(page: Page) -> List[Dict[str, str]]:
    selectors = ["nav a", "[role='navigation'] a", "aside a", "a[href^='/app/']"]
    links: List[Dict[str, str]] = []
    seen = set()
    for selector in selectors:
        locator = page.locator(selector)
        for index in range(locator.count()):
            item = locator.nth(index)
            href = item.get_attribute("href") or ""
            text = (item.inner_text() or "").strip()
            key = (href, text)
            if not href or href.startswith("http") or key in seen:
                continue
            seen.add(key)
            links.append({"href": href, "text": text})
    return links


def extract_route_metadata(page: Page) -> Dict[str, object]:
    scripts = page.locator("script[src]")
    styles = page.locator("link[rel='stylesheet']")
    bundle_scripts = []
    bundle_styles = []
    for index in range(scripts.count()):
        src = scripts.nth(index).get_attribute("src")
        if src:
            bundle_scripts.append(src)
    for index in range(styles.count()):
        href = styles.nth(index).get_attribute("href")
        if href:
            bundle_styles.append(href)
    return {
        "url": page.url,
        "title": page.title(),
        "scripts": bundle_scripts,
        "styles": bundle_styles,
    }


def attach_network_listeners(
    context: BrowserContext,
    downloads: List[Dict[str, str]],
    api_calls: List[Dict[str, object]],
) -> None:
    saved_hashes: Set[str] = set()

    def save_download(response: Response) -> None:
        try:
            content_type = response.headers.get("content-type")
            url = response.url
            target_dir = choose_download_dir(content_type, url)
            if not target_dir:
                return
            body = response.body()
            digest = hashlib.sha1(body).hexdigest()
            if digest in saved_hashes:
                return
            saved_hashes.add(digest)
            extension = guess_extension(url, content_type)
            filename = sanitize_filename(Path(urlparse(url).path).stem or digest)[:100]
            target = target_dir / f"{filename}_{digest[:10]}{extension}"
            target.write_bytes(body)
            downloads.append(
                {
                    "url": url,
                    "content_type": content_type or "",
                    "file": str(target.as_posix()),
                    "sha1": digest,
                }
            )
        except Exception:
            return

    def capture_api(response: Response) -> None:
        try:
            request = response.request
            resource_type = request.resource_type
            if resource_type not in {"fetch", "xhr"}:
                return
            api_calls.append(
                {
                    "url": response.url,
                    "method": request.method,
                    "resource_type": resource_type,
                    "status": response.status,
                    "request_headers": request.headers,
                    "response_headers": response.headers,
                    "post_data": request.post_data,
                }
            )
        except Exception:
            return

    context.on("response", save_download)
    context.on("response", capture_api)


def record_page(
    page: Page,
    output_dir: Path,
    slug: str,
    label: str,
    route: str,
    device_name: str,
    page_records: List[Dict[str, object]],
    route_records: Dict[str, Dict[str, object]],
) -> None:
    capture = capture_page(page, output_dir, slug, device_name)
    page_records.append(
        {
            "device": device_name,
            "module": slug,
            "label": label,
            "route": route,
            "capture": capture,
        }
    )
    route_records[slug] = extract_route_metadata(page)


def capture_interactions(
    page: Page,
    output_dir: Path,
    device_name: str,
    page_records: List[Dict[str, object]],
    route_records: Dict[str, Dict[str, object]],
) -> None:
    page.goto(normalize_route("/app/campaigns"), wait_until="domcontentloaded", timeout=60000)
    wait_for_page_settle(page)
    if click_first_data_row(page):
        record_page(page, output_dir, "05_campaigns_detail_modal", "Campaign detail modal", page.url, device_name, page_records, route_records)
        close_overlay_if_present(page)

    page.goto(normalize_route("/app/leads"), wait_until="domcontentloaded", timeout=60000)
    wait_for_page_settle(page)
    if click_button_by_fragments(page, ["转化", "convert"]):
        record_page(page, output_dir, "06_leads_convert_modal", "Lead convert modal", page.url, device_name, page_records, route_records)
        close_overlay_if_present(page)

    page.goto(normalize_route("/app/retail"), wait_until="domcontentloaded", timeout=60000)
    wait_for_page_settle(page)
    if click_button_by_fragments(page, ["录入", "编辑", "edit"]):
        record_page(page, output_dir, "07_retail_monthly_form", "Retail monthly form", page.url, device_name, page_records, route_records)
        close_overlay_if_present(page)

    page.goto(normalize_route("/app/accounts"), wait_until="domcontentloaded", timeout=60000)
    wait_for_page_settle(page)
    if click_text_candidate(page, ["Raffles Hospitality", "Marina Bay Sands", "Bangkok Mall Group"]):
        record_page(page, output_dir, "09_account_detail_overview", "Account detail overview", page.url, device_name, page_records, route_records)
        tab_scope = "[role='tablist'], .ant-tabs-nav"
        account_tabs = [
            (["Contacts", "联系人"], "09_account_detail_contacts"),
            (["Opportunit", "商机"], "09_account_detail_opportunities"),
            (["Contract", "合同"], "09_account_detail_contracts"),
            (["Order", "订单"], "09_account_detail_orders"),
            (["Payment", "回款"], "09_account_detail_payments"),
            (["Activit", "跟进记录"], "09_account_detail_activities"),
            (["Campaign", "市场活动"], "09_account_detail_campaigns"),
            (["Document", "文档"], "09_account_detail_documents"),
        ]
        for texts, slug in account_tabs:
            if click_text_candidate(page, texts, tab_scope):
                record_page(page, output_dir, slug, slug, page.url, device_name, page_records, route_records)

    page.goto(normalize_route("/app/settings"), wait_until="domcontentloaded", timeout=60000)
    wait_for_page_settle(page)
    settings_tabs = [
        (["品牌", "Brand"], "25_settings_brand"),
        (["角色与权限", "Role"], "25_settings_roles_permissions"),
        (["年度目标", "Target"], "25_settings_targets"),
        (["市场", "Market"], "25_settings_markets"),
        (["部门", "Department"], "25_settings_departments"),
        (["通知", "Notification"], "25_settings_notifications"),
        (["审计日志", "Audit"], "25_settings_audit_logs"),
        (["账户", "Account"], "25_settings_accounts"),
    ]
    for texts, slug in settings_tabs:
        if click_text_candidate(page, texts, "[role='tablist'], .ant-tabs-nav"):
            record_page(page, output_dir, slug, slug, page.url, device_name, page_records, route_records)

    page.goto(normalize_route("/app/orders"), wait_until="domcontentloaded", timeout=60000)
    wait_for_page_settle(page)
    record_page(page, output_dir, "18_orders_list", "Orders list", page.url, device_name, page_records, route_records)
    if click_first_data_row(page):
        record_page(page, output_dir, "18_orders_detail", "Order detail", page.url, device_name, page_records, route_records)
        close_overlay_if_present(page)

    page.goto(normalize_route("/app/project-updates"), wait_until="domcontentloaded", timeout=60000)
    wait_for_page_settle(page)
    if click_button_by_fragments(page, ["提交", "submit"], "main, [role='main']"):
        record_page(page, output_dir, "15_project_updates_form", "Project updates form", page.url, device_name, page_records, route_records)
        close_overlay_if_present(page)

    page.goto(normalize_route("/app/invoices"), wait_until="domcontentloaded", timeout=60000)
    wait_for_page_settle(page)
    if click_button_by_fragments(page, ["开票", "invoice", "新建"], "main, [role='main']"):
        record_page(page, output_dir, "19_invoices_new_form", "Invoices new form", page.url, device_name, page_records, route_records)
        close_overlay_if_present(page)


def run_capture(headless: bool, browser_path: str, mobile_only: bool, desktop_only: bool) -> None:
    ensure_directories()
    downloads: List[Dict[str, str]] = []
    api_calls: List[Dict[str, object]] = []
    page_records: List[Dict[str, object]] = []
    route_records: Dict[str, Dict[str, object]] = {}
    known_routes = {route for _, _, route in NAV_TARGETS}

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=browser_path, headless=headless)
        contexts = []
        if not mobile_only:
            contexts.append(
                (
                    "desktop",
                    DESKTOP_DIR,
                    browser.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1.5),
                )
            )
        if not desktop_only:
            contexts.append(
                (
                    "mobile",
                    MOBILE_DIR,
                    browser.new_context(
                        viewport={"width": 375, "height": 812},
                        is_mobile=True,
                        has_touch=True,
                        user_agent=(
                            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
                            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
                        ),
                        device_scale_factor=3,
                    ),
                )
            )

        for device_name, output_dir, context in contexts:
            attach_network_listeners(context, downloads, api_calls)
            page = context.new_page()
            login(page)
            record_page(page, output_dir, "00_post_login", "Post login", page.url, device_name, page_records, route_records)

            links = discover_navigation(page)
            for slug, label, route in NAV_TARGETS:
                try:
                    page.goto(normalize_route(route), wait_until="domcontentloaded", timeout=60000)
                    wait_for_page_settle(page)
                    record_page(page, output_dir, slug, label, route, device_name, page_records, route_records)
                except Exception as exc:
                    page_records.append(
                        {
                            "device": device_name,
                            "module": slug,
                            "label": label,
                            "route": route,
                            "error": str(exc),
                        }
                    )

            for link in links:
                if link["href"] in known_routes:
                    continue
                module_name = f"nav_{sanitize_filename(link['href'].replace('/app/', '').replace('/', '_'))}"
                try:
                    page.goto(normalize_route(link["href"]), wait_until="domcontentloaded", timeout=60000)
                    wait_for_page_settle(page)
                    record_page(page, output_dir, module_name, link["text"], link["href"], device_name, page_records, route_records)
                except Exception as exc:
                    page_records.append(
                        {
                            "device": device_name,
                            "module": module_name,
                            "label": link["text"],
                            "route": link["href"],
                            "error": str(exc),
                        }
                    )

            capture_interactions(page, output_dir, device_name, page_records, route_records)

            (METADATA_DIR / f"navigation_{device_name}.json").write_text(
                json.dumps(links, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            context.close()

        browser.close()

    (METADATA_DIR / "downloads.json").write_text(json.dumps(downloads, ensure_ascii=False, indent=2), encoding="utf-8")
    (METADATA_DIR / "pages.json").write_text(json.dumps(page_records, ensure_ascii=False, indent=2), encoding="utf-8")
    (API_DIR / "network_calls.json").write_text(json.dumps(api_calls, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROUTES_DIR / "route_bundles.json").write_text(json.dumps(route_records, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture AngelCRM screenshots, bundles, DOM, and static assets.")
    parser.add_argument("--headed", action="store_true", help="Run with a visible browser window.")
    parser.add_argument(
        "--browser-path",
        default=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        help="Executable path for a local Chromium-based browser.",
    )
    parser.add_argument("--mobile-only", action="store_true", help="Only capture mobile viewport.")
    parser.add_argument("--desktop-only", action="store_true", help="Only capture desktop viewport.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mobile_only and args.desktop_only:
        raise SystemExit("Choose either --mobile-only or --desktop-only, not both.")
    browser_path = Path(args.browser_path)
    if not browser_path.exists():
        raise SystemExit(f"Browser not found: {browser_path}")
    run_capture(
        headless=not args.headed,
        browser_path=str(browser_path),
        mobile_only=args.mobile_only,
        desktop_only=args.desktop_only,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
