#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Independent translated-cycler verifier: sparse tape, explicit replay.

Let d be displacement over a lap, and [l,r] bound all head locations
(including its endpoint). If d>0, require start/end tapes to agree under
translation on [l,infinity). Subsequent laps move right, so the unmatched
left wake is never read. Symmetrically for d<0. For d=0 compare [l,r].
These equalities and repeated state make induction on laps immediate.
"""
import json,re,sys

def check(c):
 if sys.flags.optimize:return False
 try:
  assert c.get('type')=='translated_cycler' and c.get('success') is True
  start,period,d=c['start'],c['period'],c['offset']
  assert all(type(x) is int for x in [start,period,d]) and start>=0 and period>0 and start+period<=1000000
  rows=c['machine'].split('_');assert 1<=len(rows)<=6
  assert all(re.fullmatch(r'(?:[01][LR][A-FZ]|---){2}',row) for row in rows)
  q=0;h=0;tape=set();past=None;initialq=None;initialh=None;low=None;high=None
  for t in range(start+period):
   if t==start:past=tape.copy();initialq=q;initialh=h;low=h;high=h
   rule=rows[q][3*int(h in tape):3*int(h in tape)+3]
   assert rule!='---' and rule[2]!='Z'
   if rule[0]=='1':tape.add(h)
   else:tape.discard(h)
   h+=1 if rule[1]=='R' else -1;q=ord(rule[2])-65;assert 0<=q<len(rows)
   if t>=start:low=min(low,h);high=max(high,h)
  assert q==initialq and h-initialh==d
  if d>0:assert {x for x in past if x>=low}=={x-d for x in tape if x-d>=low}
  elif d<0:assert {x for x in past if x<=high}=={x-d for x in tape if x-d<=high}
  else:assert {x for x in past if low<=x<=high}=={x for x in tape if low<=x<=high}
  return True
 except (KeyError,TypeError,IndexError,ValueError,AssertionError):return False
if __name__=='__main__':
 try:ok=check(json.load(open(sys.argv[1])))
 except Exception:ok=False
 print('ACCEPT' if ok else 'REJECT');sys.exit(0 if ok else 1)
