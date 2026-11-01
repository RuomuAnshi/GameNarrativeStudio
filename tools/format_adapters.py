#!/usr/bin/env python3
"""Conservative, text-only localization patches. No source overwrite."""
import argparse, collections, json, re
from pathlib import Path

TOKEN = re.compile(r'\[[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)?\]|\{/?[A-Za-z_]\w*(?:=[^{}]+)?\}|\$[A-Za-z_]\w*\$|%\([A-Za-z_]\w*\)[sdif]|%\d*\$?[sdif]|§[A-Za-z0-9!]|\\[ntr]')

def protect(old, new):
    if collections.Counter(TOKEN.findall(old)) != collections.Counter(TOKEN.findall(new)):
        raise ValueError("protected token mismatch")

def renpy(text, changes):
    if not re.search(r'^\s*translate\s+\w+\s+strings\s*:',text,re.M):
        raise ValueError("requires generated translate strings block")
    pat = re.compile(r'(^\s*old\s+"((?:\\.|[^"\\])*)"\s*\n)(\s*new\s+")((?:\\.|[^"\\])*)("[^\n]*$)',re.M)
    seen=set()
    def sub(m):
        old=json.loads('"'+m[2]+'"')
        if old not in changes:return m[0]
        val=changes[old];protect(old,val);seen.add(old)
        return m[1]+m[3]+json.dumps(val,ensure_ascii=False)[1:-1]+m[5]
    out=pat.sub(sub,text)
    if seen!=set(changes):raise ValueError("unmatched Ren'Py translation keys")
    return out

def webgal(text, changes):
    commands={'choose','changeBg','changeScene','callScene','changeFigure','changeBgm','bgm','playEffect','setVar','label','jumpLabel','setTextbox','setAnimation','setTransform','intro','unlockCg','unlockBgm','wait','end','if'}
    lines=text.splitlines(keepends=True);seen=set();out=[]
    for i,line in enumerate(lines,1):
        key=str(i)
        if key not in changes:out.append(line);continue
        m=re.match(r'^(\s*)([^:;\s]+):(.*?)(;\r?\n?|;)$',line)
        if not m or m[2] in commands:raise ValueError(f"unsupported WebGAL line {i}")
        val=changes[key]
        if any(c in val for c in (';','\n','|')):raise ValueError("unescaped WebGAL delimiter")
        protect(m[3],val);seen.add(key)
        out.append(m[1]+m[2]+':'+val+m[4])
    if seen!=set(changes):raise ValueError("unmatched WebGAL line keys")
    return ''.join(out)

def paradox(text,changes):
    if not re.match(r'^l_[a-z_]+:\s*\n',text):raise ValueError("missing Paradox language header")
    pat=re.compile(r'^(\s*)([A-Za-z0-9_.-]+)(:\d+\s+")((?:\\.|[^"\\])*)("\s*(?:#.*)?$)',re.M)
    seen=set()
    def sub(m):
        key=m[2]
        if key not in changes:return m[0]
        val=changes[key]
        if '"' in val or '\n' in val:raise ValueError("quotes/newlines unsupported")
        protect(m[4],val);seen.add(key)
        return m[1]+key+m[3]+val+m[5]
    out=pat.sub(sub,text)
    if seen!=set(changes):raise ValueError("unmatched Paradox localization keys")
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('format',choices=['renpy','webgal','paradox'])
    ap.add_argument('source');ap.add_argument('changes');ap.add_argument('output')
    a=ap.parse_args();src=Path(a.source);dst=Path(a.output)
    if src.resolve()==dst.resolve():ap.error("source overwrite forbidden")
    raw=src.read_bytes();bom=raw.startswith(b'\xef\xbb\xbf')
    if a.format=='paradox' and not bom:ap.error("Paradox localization requires BOM")
    text=raw.decode('utf-8-sig');changes=json.loads(Path(a.changes).read_text('utf-8'))
    if not isinstance(changes,dict) or not all(isinstance(k,str) and isinstance(v,str) for k,v in changes.items()):
        ap.error("changes must be a string-to-string JSON object")
    out={'renpy':renpy,'webgal':webgal,'paradox':paradox}[a.format](text,changes)
    dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_bytes((b'\xef\xbb\xbf' if bom else b'')+out.encode('utf-8'))
    print(f"OK {a.format}: {len(changes)} replacements to {dst}")
if __name__=='__main__':main()
