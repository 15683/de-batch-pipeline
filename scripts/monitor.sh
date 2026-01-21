#!/bin/bash

echo "=== Finch VM Resources ==="
finch vm status

echo -e "\n=== Container Stats ==="
finch stats --no-stream

echo -e "\n=== Disk Usage ==="
finch system df

echo -e "\n=== Memory on Host ==="
vm_stat | perl -ne '/page size of (\d+)/ and $size=$1; /Pages\s+([^:]+)[^\d]+(\d+)/ and printf("%-16s % 16.2f Mi\n", "$1:", $2 * $size / 1048576);'
