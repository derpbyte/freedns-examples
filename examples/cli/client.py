import freedns

def main():
    print("Welcome to the FreeDNS Client!")

    while True:
        print("\nOptions:")
        print("1. Log in")
        print("2. Sign up")
        print("3. Exit")

        choice = input("Choose an option (1, 2, or 3): ")

        if choice == "1":
            login()
        elif choice == "2":
            sign_up()
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    client = freedns.Client()

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

def sign_up():
    client = freedns.Client()

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
        print("\nFetching domain registry...")
        registry = client.get_registry()

        print("\nAvailable domains:")
        domain_map = {domain['domain']: domain['id'] for domain in registry['domains']}
        for domain in registry['domains']:
            print(f"Domain: {domain['domain']}")

        domain_name = input("Enter the domain name to use: ")
        subdomain_name = input("Enter the subdomain name you want to create: ")

        if domain_name not in domain_map:
            print("Invalid domain name. Please try again.")
            return

        domain_id = domain_map[domain_name]
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
            domain_id=int(domain_id),
            destination=destination
        )

        print("\nSubdomain created successfully!")

    except RuntimeError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
