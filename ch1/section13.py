from secrets import token_bytes
from typing import Tuple

def random_key(length: int) -> int:
    tb: bytes = token_bytes(length)
    return int.from_bytes(tb, "big")

def encrypt(original: str) -> Tuple[int, int]:
    original_bytes: bytes = original.encode()
    dummy: int = random_key(len(original_bytes))
    original_key: int = int.from_bytes(original_bytes, "big")
    encrypted: int = original_key ^ dummy
    return dummy, encrypted

def decrypt(key1: int, key2: int) -> str:
    decrypted: int = key1 ^ key2
    temp: bytes = decrypted.to_bytes((decrypted.bit_length()+7) // 8, "big")
    return temp.decode()

class ImageEncrypter:
    def __init__(self, src: str) -> None:
        img_bytes = self._read_img(src)
        self._encrypt(img_bytes)

    def _read_img(self, src: str) -> bytes:
        with open(src, "rb") as f:
            img_data = f.read()
        return img_data
    
    def _encrypt(self, img_bytes: bytes) -> None:
        dummy: int = random_key(len(img_bytes))
        original_key: int = int.from_bytes(img_bytes, "big")
        encrypted: int = original_key ^ dummy
        self.encrypted = encrypted
        self.dummy = dummy

    def _decrypt(self) -> bytes:
        decrypted: int = self.encrypted ^ self.dummy
        decrypt_bytes: bytes = decrypted.to_bytes((decrypted.bit_length()+7) // 8, "big")
        return decrypt_bytes

    def get_original_data(self) -> bytes:
        return self._decrypt()
        

def test_read_img():
    name_test_image = r"ch1/testimg.png"
    with open(name_test_image, "rb") as f:
        test_data = f.read()
    
def test_encrypt_image():
    name_test_image = r"ch1/testimg.png"
    name_output_image = r"ch1/encryptedimg.png"
    name_key = r"ch1/key.txt"
    with open(name_test_image, "rb") as f:
        test_data = f.read()
    img_encrypter = ImageEncrypter(name_test_image)
    assert img_encrypter.get_original_data() == test_data


if __name__ == "__main__":
    test_read_img()
    test_encrypt_image()
    key1, key2 = encrypt("This is the greates one time pad in the world!")
    result: str = decrypt(key1, key2)
    print(result)