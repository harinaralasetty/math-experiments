#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Independent n-gram CPS certificate checker. No imports from the searcher.

Invariant: local window is listed; every radius-sized block completely to
its left/right belongs to the respective language. Blank padding supplies
zero blocks. A step exposes only a block already in that language and
adds the newly written opposite block. Exhaustive successor closure
therefore preserves the invariant and excludes every halting transition.
"""
import json,re,sys

def check(c):
 if sys.flags.optimize:return False
 try:
  if c.get('type')!='ngram_cps':return False
  r=c['radius'];assert type(r) is int and 1<=r<=32
  rows=c['machine'].split('_');assert 1<=len(rows)<=6
  assert all(re.fullmatch(r'(?:[01][LR][A-FZ]|---){2}',row) for row in rows)
  assert all(t[2]=='Z' or t[2]=='-' or ord(t[2])-65<len(rows) for row in rows for t in [row[:3],row[3:]])
  L=set(c['left']);R=set(c['right']);C=set(c['contexts']);z='0'*r
  assert z in L and z in R and f'{z} [A0] {z}' in C
  assert all(re.fullmatch('[01]{'+str(r)+'}',w) for w in L|R)
  for item in C:
   m=re.fullmatch(r'([01]+) \[([A-F])([01])\] ([01]+)',item);assert m
   left,q,a,right=m.groups();assert len(left)==r and len(right)==r
   assert left in L and right in R and ord(q)-65<len(rows)
   rule=rows[ord(q)-65][int(a)*3:int(a)*3+3];assert rule!='---' and rule[2]!='Z'
   b,d,nextq=rule
   if d=='R':
    nl=left[1:]+b;read=right[0]
    for word in R:
     if word[:-1]==right[1:]:assert f'{nl} [{nextq}{read}] {word}' in C
   else:
    nr=b+right[:-1];read=left[-1]
    for word in L:
     if word[1:]==left[:-1]:assert f'{word} [{nextq}{read}] {nr}' in C
  return True
 except (KeyError,ValueError,TypeError,AssertionError,IndexError):return False
if __name__=='__main__':
 try:c=json.load(open(sys.argv[1]));ok=check(c)
 except Exception:ok=False
 print('ACCEPT' if ok else 'REJECT');sys.exit(0 if ok else 1)
