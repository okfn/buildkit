import os

BASE_DIR = '/var/lib/buildkit'
BASE_REPO_DIR = os.path.join(BASE_DIR, 'repo')
BASE_KEY_DIR = os.path.join(BASE_DIR, 'key')
DEFAULT_KEY_NAME="BuildKit-Automatic-Packaging"
DEFAULT_KEY_EMAIL="buildkit@example.com"
DEFAULT_KEY_COMMENT="Buildkit key for signing packages in the apt repo"
