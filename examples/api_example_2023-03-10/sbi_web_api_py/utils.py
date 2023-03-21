import base64


def pack_bytes(data: bytes) -> str:
    return base64.standard_b64encode(data).decode('utf-8')


def unpack_bytes(data: str) -> bytes:
    return base64.standard_b64decode(data.encode('utf-8'))
