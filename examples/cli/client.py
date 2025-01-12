import requests
import random
import os
import freedns

def load_proxies(file_path="proxy.txt"):
    """Load proxies from a file."""
    if not os.path.exists(file_path):
        print("proxy.txt not found. Requests will use the real IP.")
        return []
    else:
        print("Proxies found in proxy.txt. Checking for a working IP.")

    with open(file_path, "r") as f:
        proxies = [line.strip() for line in f if line.strip()]

    if not proxies:
        print("No proxies found in proxy.txt. Requests will use the real IP.")
    return proxies

class ProxyClient(freedns.Client):
    def __init__(self, proxies, timeout=5):
        """Init the ProxyClient with a list of proxies (proxy.txt) and a timeout."""
        super().__init__()
        self.proxies = proxies
        self.timeout = timeout
        self.session = self._get_proxy_session()

    def _get_proxy_session(self):
        """Create a requests.Session using a random proxy from the proxy.txt,"""
        session = requests.Session()
        while self.proxies:
            proxy = random.choice(self.proxies)
            proxy_parts = proxy.split(":")

            if len(proxy_parts) < 2:
                print(f"Invalid proxy format: {proxy}. Skipping.")
                self.proxies.remove(proxy)
                continue

            proxy_type = "http"
            if len(proxy_parts) == 3:
                proxy_type = proxy_parts[0]
                proxy_address = f"{proxy_parts[1]}:{proxy_parts[2]}"
            else:
                proxy_address = proxy

            session.proxies = {
                "http": f"{proxy_type}://{proxy_address}",
                "https": f"{proxy_type}://{proxy_address}"
            }
            try:
                response = session.get("https://www.google.com", timeout=self.timeout)
                if response.status_code == 200:
                    print(f"Using proxy: {proxy}")
                    return session
                else:
                    print(f"Proxy {proxy} returned status code {response.status_code}. Trying another proxy.")
            except (requests.RequestException, requests.exceptions.Timeout):
                print(f"Proxy {proxy} failed. Trying another proxy.")
                self.proxies.remove(proxy)

        print("No working proxies found. Requests will use the real IP.")
        return requests.Session()

def main():
    print("Welcome to the FreeDNS Client!")

    proxies = load_proxies()
    client = ProxyClient(proxies)

    while True:
        print("\nOptions:")
        print("1. Log in")
        print("2. Sign up")
        print("3. Exit")

        choice = input("Choose an option (1, 2, or 3): ")

        if choice == "1":
            login(client)
        elif choice == "2":
            sign_up(client)
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def login(client):
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    try:
        client.login(username=email, password=password)
        print("\nLogin successful!")

        while True:
            print("\nOptions:")
            print("1. Create a subdomain")
            print("2. Logout")

            choice = input("Choose an option (1 or 2): ")

            if choice == "1":
                create_subdomain(client)
            elif choice == "2":
                print("Logging out. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    except RuntimeError as e:
        print(f"Error: {e}")

def sign_up(client):
    try:
        print("\nRequesting captcha for account creation...")
        captcha_image = client.get_captcha()

        with open("captcha.png", "wb") as f:
            f.write(captcha_image)

        print("Captcha saved as 'captcha.png'. Please solve it.")
        captcha_code = input("Enter the captcha code: ")

        firstname = input("Enter your first name: ")
        lastname = input("Enter your last name: ")
        username = input("Enter your desired username: ")
        password = input("Enter your password: ")
        email = input("Enter your email address: ")

        client.create_account(
            captcha_code=captcha_code,
            firstname=firstname,
            lastname=lastname,
            username=username,
            password=password,
            email=email
        )

        print("\nAccount created successfully! Please check your email for the activation link.")

    except RuntimeError as e:
        print(f"Error: {e}")

def create_subdomain(client):
    try:
        domain_name = input("Enter the domain name to use: ")
        subdomain_name = input("Enter the subdomain name you want to create: ")

        record_type = input("Enter the record type (e.g., A, CNAME): ")
        destination = input("Enter the destination for the record: ")

        print("\nRequesting captcha...")
        captcha_image = client.get_captcha()

        with open("captcha.png", "wb") as f:
            f.write(captcha_image)

        print("Captcha saved as 'captcha.png'. Please solve it.")
        captcha_code = input("Enter the captcha code: ")

        client.create_subdomain(
            captcha_code=captcha_code,
            record_type=record_type,
            subdomain=subdomain_name,
            domain_id=domain_name,
            destination=destination
        )

        print("\nSubdomain created successfully!")

    except RuntimeError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
