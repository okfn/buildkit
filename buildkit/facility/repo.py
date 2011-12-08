import os

def key_exists(repo, key_dir, repo_dir):
    for filename in [
        os.path.join(repo_dir, 'packages_public.key'),
        os.path.join(key_dir, 'buildkit.pub'),
        os.path.join(key_dir, 'buildkit.sec'),
    ]:
        if os.path.exists(filename):
            return True
    return False
