#!/usr/bin/env python3
"""FETCH RESULT — download a finished Higgsfield job's output from its job json.
$0.  Usage: fetch_result.py <job.json> <out.png|out.mp4>
An empty [] json is a DROPPED WAIT, not a failed job (law 5): check `higgsfield generate list`."""
import json, sys, urllib.request
j = json.load(open(sys.argv[1]))
if not j: sys.exit(f"{sys.argv[1]}: EMPTY job json — dropped wait; recover with `higgsfield generate wait <id> --json`")
j = j[0] if isinstance(j, list) else j
url = j.get("result_url") or j.get("min_result_url")
if not url: sys.exit(f"no result_url in {sys.argv[1]} (status {j.get('status')})")
urllib.request.urlretrieve(url, sys.argv[2]); print(f"{sys.argv[2]}  <- job {j.get('id','?')[:8]}  {url.split('/')[-1]}")
