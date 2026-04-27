"""Shared authentication helpers for ADO, GitHub, and MS Graph."""

import os
from functools import lru_cache

from azure.devops.connection import Connection
from azure.identity import ClientSecretCredential
from msrest.authentication import BasicAuthentication


@lru_cache(maxsize=1)
def get_ado_connection() -> Connection:
    org_url = os.environ["ADO_ORG_URL"]
    pat = os.environ["ADO_PAT"]
    credentials = BasicAuthentication("", pat)
    return Connection(base_url=org_url, creds=credentials)


@lru_cache(maxsize=1)
def get_ms_graph_credential() -> ClientSecretCredential:
    return ClientSecretCredential(
        tenant_id=os.environ["AZURE_TENANT_ID"],
        client_id=os.environ["AZURE_CLIENT_ID"],
        client_secret=os.environ["AZURE_CLIENT_SECRET"],
    )


def get_github_token() -> str:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        raise EnvironmentError("GITHUB_TOKEN or GITHUB_PERSONAL_ACCESS_TOKEN must be set")
    return token
