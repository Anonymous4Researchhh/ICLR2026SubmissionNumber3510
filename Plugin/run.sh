#!/usr/bin/env sh

# Override locale
export LC_ALL=C

# Move to the script directory
cd "$(dirname "$(readlink -f "$0")")" || exit

# Run the app
exec ./Besiege.x86_64 "$@"
