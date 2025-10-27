import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import hashlib

from select_folder import choose_folder

# === 1. g ni saqlash / o'qish ===
def save_g(g_value: bytes, folder="keys", filename="g.key"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    with open(path, "wb") as f:
        f.write(g_value)
    return path

def load_g(folder="keys", filename="g.key"):
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    else:
        g_value = b"my_fixed_generator_value_12345"
        save_g(g_value, folder, filename)
        return g_value

# === 2. Deterministik private scalar ===
SECP256R1_ORDER = int(
    "FFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551", 16
)

def generate_private_scalar(g_bytes: bytes) -> int:
    digest = hashlib.sha256(g_bytes).digest()
    scalar = int.from_bytes(digest, "big") % SECP256R1_ORDER
    if scalar == 0:
        scalar = 1
    return scalar

# === 3. Keypair yaratish ===
def generate_deterministic_keypair(g_value: bytes):
    scalar = generate_private_scalar(g_value)
    private_key = ec.derive_private_key(scalar, ec.SECP256R1())
    public_key = private_key.public_key()
    return private_key, public_key

# === 4. Faylga saqlash funksiyalari ===
def save_private_key(private_key, folder="keys"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "private.key")
    with open(path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    return path

def save_public_key_to_path(public_key, path):
    """
    Public keyni foydalanuvchi beradigan pathga saqlaydi.
    Agar faqat katalog kiritilsa, fayl nomi 'public.key' qo'shiladi.
    """
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    # Agar path katalog bo'lsa, fayl nomini qo‘shamiz
    if os.path.isdir(path):
        path = os.path.join(path, "public.key")

    with open(path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    return path

def ecdh_key_generate():
    # g ni o'qish yoki yaratish keys/ ichida
    g_value = load_g(folder="keys")
    
    # Keypair yaratish
    private_key, public_key = generate_deterministic_keypair(g_value)
    
    # Private keyni keys/ ichida saqlash
    private_path = save_private_key(private_key, folder="keys")
    
    # Public key uchun foydalanuvchidan path so‘rash
    user_path = choose_folder()
    public_path = save_public_key_to_path(public_key, user_path)

# # === 5. Demo ===
# if __name__ == "__main__":
#     # g ni o'qish yoki yaratish keys/ ichida
#     g_value = load_g(folder="keys")
    
#     # Keypair yaratish
#     private_key, public_key = generate_deterministic_keypair(g_value)
    
#     # Private keyni keys/ ichida saqlash
#     private_path = save_private_key(private_key, folder="keys")
    
#     # Public key uchun foydalanuvchidan path so‘rash
#     user_path = choose_folder()
#     public_path = save_public_key_to_path(public_key, user_path)

#     print("\n✅ Saqlash bajarildi!")
#     print("g.key:", os.path.abspath(os.path.join("keys", "g.key")))
#     print("Private key:", os.path.abspath(private_path))
#     print("Public key:", os.path.abspath(public_path))
