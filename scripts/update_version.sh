#!/bin/bash
#
# Update Thai DRG Grouper version
# Usage: ./update_version.sh <version> <source>
#

set -e

VERSION=$1
SOURCE=$2
SET_DEFAULT=${3:-"yes"}

echo "🏥 Thai DRG Grouper - Update Script"
echo "===================================="

if [ -z "$VERSION" ] || [ -z "$SOURCE" ]; then
    echo ""
    echo "Usage: $0 <version> <source> [set_default]"
    echo ""
    echo "Examples:"
    echo "  $0 6.4 /downloads/TGrp64.zip"
    echo "  $0 6.4 https://www.tcmc.or.th/.../TGrp64.zip"
    exit 1
fi

# Download if URL
if [[ "$SOURCE" == http* ]]; then
    echo "📥 Downloading..."
    TEMP_FILE="/tmp/tgrp_${VERSION}.zip"
    curl -L -o "$TEMP_FILE" "$SOURCE"
    SOURCE="$TEMP_FILE"
fi

# Add version
CMD="thai-drg-grouper add --version $VERSION --source $SOURCE"
if [ "$SET_DEFAULT" == "yes" ]; then
    CMD="$CMD --set-default"
fi

echo "📦 Adding version $VERSION..."
$CMD

# Cleanup
if [ -f "/tmp/tgrp_${VERSION}.zip" ]; then
    rm "/tmp/tgrp_${VERSION}.zip"
fi

echo ""
echo "✅ Done!"
thai-drg-grouper list
