#!/usr/bin/env python3
"""Compare local ANGEL CRM screenshots with captured source-system screenshots.

Outputs a JSON report and side-by-side diff images under output/screenshots/diffs/.
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

LOCAL_DIR = Path("output/screenshots")
SOURCE_DIR = Path("output/desktop")
DIFF_DIR = LOCAL_DIR / "diffs"
REPORT_PATH = DIFF_DIR / "report.json"

TARGET_SIZE = (1440, 810)
THRESHOLD = 35

PAIRS = [
    ("login", "00_post_login_full.png"),
    ("today", "01_today_full.png"),
    ("dashboard", "02_dashboard_full.png"),
    ("workqueue", "03_work_queue_full.png"),
    ("campaigns", "05_campaigns_full.png"),
    ("leads", "06_leads_full.png"),
    ("accounts", "08_accounts_full.png"),
    ("account_detail", "09_account_detail_overview_full.png"),
    ("contacts", "11_contacts_full.png"),
    ("pipeline", "13_pipeline_full.png"),
    ("contracts", "17_contracts_full.png"),
    ("orders", "18_orders_full.png"),
    ("payments", "20_payments_full.png"),
    ("products", "21_products_full.png"),
    ("settings", "25_settings_full.png"),
    ("pool", "10_pool_full.png"),
    ("end_users", "12_end_users_full.png"),
    ("team", "24_team_full.png"),
    ("country_reports", "22_country_reports_full.png"),
    ("executive_report", "23_executive_report_full.png"),
    ("retail", "07_retail_full.png"),
    ("project_updates", "15_project_updates_full.png"),
    ("import", "nav_import_full.png"),
    ("invite", "nav_invite_full.png"),
    ("attendance", "04_attendance_full.png"),
    ("log_activity", "14_log_activity_full.png"),
    ("invoices", "19_invoices_full.png"),
]


def normalize_size(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Resize or center-crop/pad to the target size."""
    img = img.convert("RGB")
    if img.size == size:
        return img
    # Prefer resize preserving aspect ratio then center crop
    src_w, src_h = img.size
    tgt_w, tgt_h = size
    scale = max(tgt_w / src_w, tgt_h / src_h)
    new_w = int(src_w * scale)
    new_h = int(src_h * scale)
    resized = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - tgt_w) // 2
    top = (new_h - tgt_h) // 2
    return resized.crop((left, top, left + tgt_w, top + tgt_h))


def compare_pair(local_path: Path, source_path: Path):
    if not local_path.exists():
        return None
    if not source_path.exists():
        return None

    local = normalize_size(Image.open(local_path), TARGET_SIZE)
    source = normalize_size(Image.open(source_path), TARGET_SIZE)

    pixels_local = local.load()
    pixels_source = source.load()
    w, h = TARGET_SIZE
    diff_count = 0
    max_diff = 0
    diff_img = local.copy()
    draw = ImageDraw.Draw(diff_img, "RGBA")

    for y in range(h):
        for x in range(w):
            r1, g1, b1 = pixels_local[x, y]
            r2, g2, b2 = pixels_source[x, y]
            diff = max(abs(r1 - r2), abs(g1 - g2), abs(b1 - b2))
            if diff > max_diff:
                max_diff = diff
            if diff > THRESHOLD:
                diff_count += 1
                # Semi-transparent red highlight
                draw.point((x, y), fill=(238, 39, 55, 180))

    total = w * h
    ratio = diff_count / total if total else 0.0
    similarity = max(0.0, 1.0 - ratio)
    return {
        "diff_count": diff_count,
        "total_pixels": total,
        "diff_ratio": round(ratio, 4),
        "similarity": round(similarity, 4),
        "max_pixel_diff": max_diff,
        "diff_image": str(DIFF_DIR / f"diff_{local_path.stem}.png"),
    }


def build_collage(local_path: Path, source_path: Path, diff_img: Image.Image) -> Image.Image:
    local = normalize_size(Image.open(local_path), TARGET_SIZE)
    source = normalize_size(Image.open(source_path), TARGET_SIZE)
    w, h = TARGET_SIZE
    collage = Image.new("RGB", (w * 3, h))
    collage.paste(source, (0, 0))
    collage.paste(local, (w, 0))
    collage.paste(diff_img, (w * 2, 0))
    return collage


def main():
    DIFF_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    for local_name, source_name in PAIRS:
        local_path = LOCAL_DIR / f"{local_name}.png"
        source_path = SOURCE_DIR / source_name
        print(f"Comparing {local_name} ...")
        result = compare_pair(local_path, source_path)
        if result is None:
            print(f"  skipped (missing {'local' if not local_path.exists() else 'source'})")
            results.append({
                "page": local_name,
                "source": str(source_path),
                "status": "skipped",
            })
            continue

        # Build and save side-by-side collage
        diff_img = Image.open(result["diff_image"]) if Path(result["diff_image"]).exists() else None
        if diff_img is None:
            diff_img = normalize_size(Image.open(local_path), TARGET_SIZE)
        collage = build_collage(local_path, source_path, diff_img)
        collage_path = DIFF_DIR / f"collage_{local_name}.png"
        collage.save(collage_path, "PNG")

        result.update({
            "page": local_name,
            "local": str(local_path),
            "source": str(source_path),
            "status": "ok",
            "collage": str(collage_path),
        })
        results.append(result)
        print(f"  similarity {result['similarity']*100:.1f}% ({result['diff_ratio']*100:.1f}% pixels differ)")

    # Summary
    ok_results = [r for r in results if r.get("status") == "ok"]
    if ok_results:
        avg_similarity = sum(r["similarity"] for r in ok_results) / len(ok_results)
        overall = {
            "average_similarity": round(avg_similarity, 4),
            "average_diff_ratio": round(sum(r["diff_ratio"] for r in ok_results) / len(ok_results), 4),
            "pages_compared": len(ok_results),
        }
    else:
        overall = {}

    report = {"summary": overall, "pages": results}
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nReport written to {REPORT_PATH}")
    if overall:
        print(f"Average pixel-level similarity: {overall['average_similarity']*100:.1f}%")


if __name__ == "__main__":
    main()
