import re

from bs4 import BeautifulSoup
from urllib.parse import urlparse


def analyze_html(html_content):

    results = {
        "has_forms": False,
        "has_javascript": False,
        "has_base64_images": False,
        "hidden_elements": [],
        "mismatched_links": [],
        "external_resources": [],
        "reasons": []
    }

    if not html_content:

        return results

    soup = BeautifulSoup(
        html_content,
        "html.parser"
    )

    # -------------------------
    # Forms Detection
    # -------------------------
    forms = soup.find_all("form")

    if forms:

        results["has_forms"] = True

        results["reasons"].append(
            "Email contains HTML forms"
        )

    # -------------------------
    # JavaScript Detection
    # -------------------------
    scripts = soup.find_all("script")

    if scripts:

        results["has_javascript"] = True

        results["reasons"].append(
            "Email contains JavaScript"
        )

    # -------------------------
    # Hidden Elements
    # -------------------------
    hidden_tags = soup.find_all(
        style=lambda value:
        value and (
            "display:none" in value.lower()
            or "visibility:hidden" in value.lower()
        )
    )

    for tag in hidden_tags:

        text = tag.get_text(strip=True)

        if text:

            results["hidden_elements"].append(text)

    if results["hidden_elements"]:

        results["reasons"].append(
            "Email contains hidden HTML elements"
        )

    # -------------------------
    # Base64 Embedded Images
    # -------------------------
    images = soup.find_all("img")

    for img in images:

        src = img.get("src", "")

        if "base64" in src:

            results["has_base64_images"] = True

            results["reasons"].append(
                "Email contains base64 embedded content"
            )

    # -------------------------
    # Mismatched Links
    # -------------------------
    links = soup.find_all("a")

    for link in links:

        href = link.get("href", "")

        visible_text = link.get_text(strip=True)

        if not href:
            continue

        # if visible text itself looks like a URL
        if visible_text.startswith("http"):

            visible_domain = urlparse(
                visible_text
            ).netloc

            href_domain = urlparse(
                href
            ).netloc

            if visible_domain != href_domain:

                results["mismatched_links"].append({
                    "text": visible_text,
                    "actual": href
                })

    if results["mismatched_links"]:

        results["reasons"].append(
            "Email contains mismatched hyperlinks"
        )

    # -------------------------
    # External Resources
    # -------------------------
    for tag in soup.find_all(["img", "script", "iframe"]):

        src = tag.get("src")

        if src and src.startswith("http"):

            results["external_resources"].append(src)

    if results["external_resources"]:

        results["reasons"].append(
            "Email loads external resources"
        )

    return results