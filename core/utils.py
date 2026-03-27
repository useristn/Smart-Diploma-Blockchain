import hashlib
import json
import secrets
import string
from decimal import Decimal
from uuid import UUID


def json_default(value):
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, UUID):
        return str(value)
    raise TypeError(f"Unsupported value for canonical JSON: {type(value)!r}")


def canonicalize_json(payload) -> str:
    return json.dumps(
        payload or {},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=json_default,
    )


def sha256_digest(value) -> str:
    if isinstance(value, str):
        value = value.encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def short_fingerprint(value: str, head: int = 10, tail: int = 6) -> str:
    if not value:
        return ""
    if len(value) <= head + tail:
        return value
    return f"{value[:head]}...{value[-tail:]}"


def mask_value(value: str, visible_prefix: int = 2, visible_suffix: int = 2) -> str:
    if not value:
        return ""
    if len(value) <= visible_prefix + visible_suffix:
        return "*" * len(value)
    hidden = "*" * max(0, len(value) - visible_prefix - visible_suffix)
    return f"{value[:visible_prefix]}{hidden}{value[-visible_suffix:]}"


def generate_random_code(prefix: str, length: int = 8) -> str:
    alphabet = string.ascii_uppercase + string.digits
    token = "".join(secrets.choice(alphabet) for _ in range(length))
    return f"{prefix}-{token}"


def compute_merkle_root(hashes: list) -> str:
    """Compute the Merkle root from a list of hex-encoded SHA-256 hashes.

    Leaves are sorted for determinism. Odd layers duplicate the last leaf.
    An empty list returns SHA-256("").
    """
    if not hashes:
        return sha256_digest("")
    layer = sorted(hashes)
    while len(layer) > 1:
        next_layer = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            right = layer[i + 1] if i + 1 < len(layer) else layer[i]
            next_layer.append(sha256_digest(left + right))
        layer = next_layer
    return layer[0]


def compute_merkle_proof(hashes: list, target_hash: str) -> list:
    """Return the sibling path proving *target_hash* is in the Merkle tree.

    Each element is {"hash": <hex>, "direction": "left"|"right"}.
    Returns [] if target_hash is not in the list.
    """
    if not hashes or target_hash not in hashes:
        return []
    layer = sorted(hashes)
    idx = layer.index(target_hash)
    proof = []
    while len(layer) > 1:
        next_idx = idx // 2
        next_layer = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            right = layer[i + 1] if i + 1 < len(layer) else layer[i]
            if i == idx:
                sibling = layer[i + 1] if i + 1 < len(layer) else layer[i]
                proof.append({"hash": sibling, "direction": "right"})
            elif i + 1 == idx:
                proof.append({"hash": left, "direction": "left"})
            next_layer.append(sha256_digest(left + right))
        idx = next_idx
        layer = next_layer
    return proof
