from rest_framework.throttling import AnonRateThrottle


class PublicVerificationThrottle(AnonRateThrottle):
    """Custom throttle for public verification endpoints."""

    scope = "public_verification"
