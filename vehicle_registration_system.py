import hashlib

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


# ============================================================
# GLOBAL DATA
# ============================================================

vehicles = {}

private_key = None
public_key = None

last_message = None
last_signature = None


# ============================================================
# SHA-256 HASHING
# ============================================================

def generate_sha256():

    print("\n" + "=" * 60)
    print("SHA-256 HASH".center(60))
    print("=" * 60)

    message = input("Enter a message: ")

    if not message.strip():
        print("\n❌ Message cannot be empty.")
        return

    sha256_hash = hashlib.sha256(message.encode()).hexdigest()

    print("\nOriginal Message:")
    print(message)

    print("\nSHA-256 Hash:")
    print(sha256_hash)


# ============================================================
# GENERATE RSA KEY PAIR
# ============================================================

def generate_keys():

    global private_key
    global public_key

    print("\n" + "=" * 60)
    print("GENERATING RSA KEY PAIR".center(60))
    print("=" * 60)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    print("\n✅ Public-private key pair generated successfully.")

    print("\nPrivate Key:")
    print(private_key)

    print("\nPublic Key:")
    print(public_key)


# ============================================================
# DIGITAL SIGNATURE
# ============================================================

def sign_message():

    global private_key
    global last_message
    global last_signature

    print("\n" + "=" * 60)
    print("DIGITAL SIGNATURE".center(60))
    print("=" * 60)

    # Generate keys automatically if they don't exist
    if private_key is None:
        print("\nNo key pair found.")
        print("Generating a new RSA key pair...")

        generate_keys()

    message = input("\nEnter message to sign: ")

    if not message.strip():
        print("\n❌ Message cannot be empty.")
        return

    last_message = message

    last_signature = private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    print("\n✅ Message signed successfully.")

    print("\nSignature:")
    print(last_signature.hex())


# ============================================================
# VERIFY DIGITAL SIGNATURE
# ============================================================

def verify_signature():

    global public_key
    global last_message
    global last_signature

    print("\n" + "=" * 60)
    print("VERIFY DIGITAL SIGNATURE".center(60))
    print("=" * 60)

    if public_key is None:
        print("\n❌ No public key found.")
        print("Please generate keys and sign a message first.")
        return

    if last_signature is None or last_message is None:
        print("\n❌ No signature found.")
        print("Please sign a message first.")
        return

    print("\nOriginal signed message:")
    print(last_message)

    message = input(
        "\nEnter the message again for verification: "
    )

    if not message.strip():
        print("\n❌ Message cannot be empty.")
        return

    try:

        public_key.verify(
            last_signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        print("\n✅ Digital Signature is VALID.")

    except InvalidSignature:

        print("\n❌ Digital Signature is INVALID.")


# ============================================================
# REGISTER VEHICLE
# ============================================================

def register_vehicle():

    print("\n" + "=" * 60)
    print("REGISTER VEHICLE".center(60))
    print("=" * 60)

    number_plate = input(
        "Enter vehicle number plate: "
    ).strip().upper()

    if not number_plate:
        print("\n❌ Number plate cannot be empty.")
        return

    # Check duplicate number plate
    if number_plate in vehicles:
        print("\n❌ This number plate is already registered.")
        return

    owner = input("Enter owner name: ").strip()

    if not owner:
        print("\n❌ Owner name cannot be empty.")
        return

    model = input("Enter vehicle model: ").strip()

    if not model:
        print("\n❌ Vehicle model cannot be empty.")
        return

    # Store vehicle information
    vehicles[number_plate] = {
        "owner": owner,
        "model": model
    }

    print("\n✅ Vehicle registered successfully.")

    print("\nVehicle Details:")
    print("-" * 40)
    print(f"Number Plate : {number_plate}")
    print(f"Owner        : {owner}")
    print(f"Model        : {model}")


# ============================================================
# RETRIEVE VEHICLE
# ============================================================

def get_vehicle():

    print("\n" + "=" * 60)
    print("GET VEHICLE".center(60))
    print("=" * 60)

    number_plate = input(
        "Enter vehicle number plate: "
    ).strip().upper()

    if not number_plate:
        print("\n❌ Number plate cannot be empty.")
        return

    if number_plate not in vehicles:
        print("\n❌ Vehicle not found.")
        return

    vehicle = vehicles[number_plate]

    print("\n✅ Vehicle Found!")

    print("\nVehicle Details:")
    print("-" * 40)
    print(f"Number Plate : {number_plate}")
    print(f"Owner        : {vehicle['owner']}")
    print(f"Model        : {vehicle['model']}")


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        print("\n")
        print("=" * 60)
        print("CRYPTOGRAPHY & VEHICLE REGISTRATION".center(60))
        print("=" * 60)

        print("1. Generate SHA-256 Hash")
        print("2. Generate Public-Private Key Pair")
        print("3. Sign Message")
        print("4. Verify Digital Signature")
        print("5. Register Vehicle")
        print("6. Get Vehicle")
        print("7. Exit")

        print("=" * 60)

        choice = input("Enter your choice: ").strip()

        # SHA-256
        if choice == "1":
            generate_sha256()

        # Generate Keys
        elif choice == "2":
            generate_keys()

        # Sign Message
        elif choice == "3":
            sign_message()

        # Verify Signature
        elif choice == "4":
            verify_signature()

        # Register Vehicle
        elif choice == "5":
            register_vehicle()

        # Get Vehicle
        elif choice == "6":
            get_vehicle()

        # Exit
        elif choice == "7":
            print("\nThank you for using the system.")
            print("Goodbye! 👋")
            break

        # Invalid Choice
        else:
            print("\n❌ Invalid choice.")
            print("Please select an option from 1 to 7.")


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()
