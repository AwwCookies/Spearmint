#!/usr/bin/env python
import sys
import json

import spearmint

data = json.loads(sys.argv[1])

if data["type"] == "CHANJOIN":
    spearmint.chanmsg(data["channel"], "Hello!")
