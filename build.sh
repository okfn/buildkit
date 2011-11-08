#!/bin/bash

VERSION=0.2.1
PACKAGEVERSION=01

if [ ! -d "dist/buildkit" ] 
then 
    mkdir -p dist/buildkit
fi

echo "Packaging version: $PACKAGEVERSION"
python -m buildkit.run pkg nonpython -p "$PACKAGEVERSION" -o dist/buildkit --deb buildkit_deb
python -m buildkit.run pkg python -p "$PACKAGEVERSION" -o dist/buildkit --author-email james@jimmyg.org --deb .
#sudo -u buildkit python -m buildkit.run repo add /var/lib/buildkit/repo/buildkit-${VERSION} dist/buildkit/*buildkit_*${PACKAGEVERSION}*.deb
#if [ ! -d "/var/lib/buildkit/repo/buildkit-${VERSION}" ] 
#then 
#    sudo cp -pr /var/lib/buildkit/repo/base_lucid "/var/lib/buildkit/repo/buildkit-${VERSION}"
#fi
sudo dpkg -i dist/buildkit/*buildkit_*${PACKAGEVERSION}*.deb
