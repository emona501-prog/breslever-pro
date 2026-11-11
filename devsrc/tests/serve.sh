#!/bin/bash
pkill -f "http.server 8900" 2>/dev/null; cd /home/claude/breslever-pro/www && (nohup python3 -m http.server 8900 >/dev/null 2>&1 &) ; sleep 1
