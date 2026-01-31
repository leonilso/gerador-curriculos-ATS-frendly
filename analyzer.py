import argparse
import sys
import json
from extractor import extract_requirements


def fetch_with_playwright(url: str) -> str:
    from playwright.sync_api import sync_playwright
    import random
    import time

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True, 
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ]
        )

        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            extra_http_headers={
                "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "Upgrade-Insecure-Requests": "1",
                "DNT": "1",
            },
        )

        page = context.new_page()

        page.goto(url, wait_until="domcontentloaded", timeout=60000)

        time.sleep(random.uniform(0.8, 1.6))

        page.wait_for_selector("h1", timeout=20000)

        page.mouse.wheel(0, random.randint(200, 600))
        time.sleep(random.uniform(0.3, 0.7))

        html = page.content()

        context.close()
        browser.close()

        return html


def read_input(args):
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return f.read(), True

    if args.url:
        html = fetch_with_playwright(args.url)
        return html, True

    if args.text:
        return args.text, False

    if not sys.stdin.isatty():
        return sys.stdin.read(), True

    raise ValueError("Forneça --file, --url, --text ou stdin")


def main():
    parser = argparse.ArgumentParser(
        description="Extrator de requisitos de vagas (ATS-friendly)"
    )
    parser.add_argument("--file", help="HTML da vaga")
    parser.add_argument("--url", help="URL da vaga (JS suportado via Playwright)")
    parser.add_argument("--text", help="Texto puro da vaga")
    parser.add_argument("--json", action="store_true", help="Output JSON")

    args = parser.parse_args()

    content, is_html = read_input(args)

    result = extract_requirements(content, is_html=is_html)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for k, v in result.items():
            print(f"\n{k.upper()}")
            if isinstance(v, list):
                for item in v:
                    print(f" - {item}")
            else:
                print(v)


if __name__ == "__main__":
    main()
