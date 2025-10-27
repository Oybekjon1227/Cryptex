import os
from open_file import file_path
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
import hashlib

def load_g_and_private(folder="keys", g_filename="g.key", priv_filename="private.key"):
    """
    keys/ papkadan g va private keyni o'qib oladi
    """
    # g ni o'qish
    g_path = os.path.join(folder, g_filename)
    if not os.path.exists(g_path):
        raise FileNotFoundError(f"{g_path} mavjud emas")
    with open(g_path, "rb") as f:
        g = f.read()
    
    # private keyni o'qish
    priv_path = os.path.join(folder, priv_filename)
    if not os.path.exists(priv_path):
        raise FileNotFoundError(f"{priv_path} mavjud emas")
    with open(priv_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    
    return g, private_key

def load_peer_public_key(path):
    """
    Foydalanuvchi beradigan pathdan peer public keyni o'qish
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} mavjud emas")
    with open(path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    return public_key

def deterministic_private_from_g(g_bytes):
    """
    g orqali deterministik private scalar hosil qiladi
    """
    SECP256R1_ORDER = int(
        "FFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551", 16
    )
    digest = hashlib.sha256(g_bytes).digest()
    scalar = int.from_bytes(digest, "big") % SECP256R1_ORDER
    if scalar == 0:
        scalar = 1
    private_key = ec.derive_private_key(scalar, ec.SECP256R1())
    return private_key

def generate_aes256_key(private_key, peer_public_key):
    """
    ECDH orqali AES-256 kalit hosil qiladi
    """
    shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)
    digest = hashes.Hash(hashes.SHA256())
    digest.update(shared_secret)
    aes_key = digest.finalize()
    return aes_key

def save_aes_key(aes_key, folder="keys", filename="secret.key"):
    """
    AES-256 keyni faylga saqlaydi
    """
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    with open(path, "wb") as f:
        f.write(aes_key)
    return path

def aes_key_generate():
    # 1️⃣ g va private keyni keys/ papkadan o'qish
    g, private_key_from_file = load_g_and_private(folder="keys")
    
    # 2️⃣ Agar private keyni g orqali qayta hosil qilmoqchi bo'lsangiz
    # private_key = deterministic_private_from_g(g)
    private_key = private_key_from_file  # agar allaqachon private.key mavjud bo'lsa
    
    # 3️⃣ Peer public key pathini foydalanuvchidan olish
    peer_public_path = file_path()
    peer_public_key = load_peer_public_key(peer_public_path)
    
    # 4️⃣ AES-256 key hosil qilish
    aes_key = generate_aes256_key(private_key, peer_public_key)
    
    # 5️⃣ AES keyni keys/secret.key faylga saqlash
    secret_path = save_aes_key(aes_key, folder="keys", filename="secret.key")

# ===== Misol ishlatish =====
if __name__ == "__main__":
    # 1️⃣ g va private keyni keys/ papkadan o'qish
    g, private_key_from_file = load_g_and_private(folder="keys")
    
    # 2️⃣ Agar private keyni g orqali qayta hosil qilmoqchi bo'lsangiz
    # private_key = deterministic_private_from_g(g)
    private_key = private_key_from_file  # agar allaqachon private.key mavjud bo'lsa
    
    # 3️⃣ Peer public key pathini foydalanuvchidan olish
    peer_public_path = file_path()
    peer_public_key = load_peer_public_key(peer_public_path)
    
    # 4️⃣ AES-256 key hosil qilish
    aes_key = generate_aes256_key(private_key, peer_public_key)
    
    # 5️⃣ AES keyni keys/secret.key faylga saqlash
    secret_path = save_aes_key(aes_key, folder="keys", filename="secret.key")
    
    print("\n✅ AES-256 key hosil qilindi va saqlandi!")
    print("Fayl:", os.path.abspath(secret_path))
