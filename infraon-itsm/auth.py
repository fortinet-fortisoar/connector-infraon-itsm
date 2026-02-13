"""
Copyright start
MIT License
Copyright (c) 2026 Fortinet Inc
Copyright end
"""

import requests
import time
from threading import Lock
from connectors.core.connector import ConnectorError, get_logger
from .constants import LOGGER_NAME, ENDPOINTS

logger = get_logger(LOGGER_NAME)

# Token cache with thread safety (Standard Alloy Pattern)
_token_cache = {}
_cache_lock = Lock()


class InfraonAuth:
    """
    Handles authentication for Infraon ITSM API
    """

    def __init__(self, config):
        self.server_url = config.get('server_url', '').strip().rstrip('/')
        if not self.server_url.startswith(('http://', 'https://')):
            self.server_url = f"https://{self.server_url}"

        self.username = config.get('username')
        self.password = config.get('password')
        self.verify_ssl = config.get('verify_ssl', False)

    def _get_cached_token(self):
        """Return cached token if still valid"""
        with _cache_lock:
            cache_key = f"{self.server_url}_{self.username}"
            token_data = _token_cache.get(cache_key)
            if token_data:
                # Assuming a default validity since Infraon logic didn't specify expiry
                # We simply return the cached token if it exists
                return token_data.get("token")
        return None

    def _cache_token(self, token):
        """Store token in cache"""
        with _cache_lock:
            cache_key = f"{self.server_url}_{self.username}"
            _token_cache[cache_key] = {
                "token": token,
                "created_at": time.time()
            }
        return token

    def _generate_token(self):
        """
        Request new token from Infraon API
        Logic taken from original _generate_token
        """
        auth_url = f"{self.server_url}{ENDPOINTS['auth']}"
        auth_payload = {"username": self.username, "password": self.password}

        try:
            response = requests.post(auth_url, json=auth_payload, verify=self.verify_ssl)
            if response.ok:
                token = response.json().get("token")
                if not token:
                    raise ConnectorError("Authentication successful, but no token was returned.")
                return self._cache_token(token)
            else:
                raise ConnectorError(f"API Error: Failed to generate token ({response.status_code})")
        except Exception as e:
            raise ConnectorError(str(e))

    def get_access_token(self):
        """Get valid access token (cache or new)"""
        token = self._get_cached_token()
        if token:
            return token
        return self._generate_token()

    def get_auth_header(self):
        """Get the authorization header for API requests"""
        token = self.get_access_token()
        # Original logic used the token directly in Authorization header, not Bearer
        return {
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
