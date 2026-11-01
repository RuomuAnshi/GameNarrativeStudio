#!/usr/bin/env python3
"""JSON scene validation and small Ren'Py export. Not a full engine compiler."""
import argparse,copy,json,re,sys
from pathlib import Path
IDENT=re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
TOKEN=re.compile(r'\{[A-Za-z_]\w*\}|\[[A-Za-z_]\w*\]|%\([A-Za-z_]\w*\)[a-z]|<[^>]+>|\\[ntr]')
def read(p):return json.loads(Path(p).read_text('utf-8'))
def validate(scene):
    errors=[];warnings=[];nodes=scene.get('nodes',{});start=scene.get('start')
    if not isinstance(nodes,dict) or not nodes:return ['missing nodes'],[]
    if start not in nodes:errors.append('missing start')
    for key,n in nodes.items():
        if not IDENT.fullmatch(key):errors.append(f'invalid id {key}')
        t=n.get('type')
        if t=='line':
            if not isinstance(n.get('text'),str):errors.append(f'{key}: text missing')
            if n.get('next') not in nodes:errors.append(f'{key}: next missing')
        elif t=='choice':
            if not n.get('options'):errors.append(f'{key}: empty choices')
            for o in n.get('options',[]):
                if o.get('target') not in nodes:errors.append(f'{key}: target missing')
        elif t!='end':errors.append(f'{key}: unknown type')
    seen=set();stack=[start]
    while stack:
        k=stack.pop()
        if k not in nodes or k in seen:continue
        seen.add(k);n=nodes[k]
        if n['type']=='line':stack.append(n.get('next'))
        if n['type']=='choice':stack.extend(o.get('target') for o in n.get('options',[]))
    warnings=[f'unreachable: {k}' for k in nodes if k not in seen]
    return errors,warnings
def quote(s):return json.dumps(s,ensure_ascii=False).replace('[','[[')
def export(scene):
    errors,_=validate(scene)
    if errors:raise ValueError('; '.join(errors))
    out=[f'label gns_{scene["start"]}:',f'    jump gns_node_{scene["start"]}','']
    for k,n in scene['nodes'].items():
        out.append(f'label gns_node_{k}:')
        if n['type']=='line':
            speaker=n.get('speaker')
            out.append('    '+(speaker+' ' if speaker and IDENT.fullmatch(speaker) else '')+quote(n['text']))
            out.append('    jump gns_node_'+n['next'])
        elif n['type']=='choice':
            out.append('    menu:')
            for o in n['options']:
                out.extend(['        '+quote(o['text'])+':','            jump gns_node_'+o['target']])
        else:out.append('    return')
        out.append('')
    return '\n'.join(out)
def patch_json(src,changes):
    obj=copy.deepcopy(src);seen=set()
    for line in obj.get('lines',[]):
        k=line.get('id')
        if k in changes:
            old=line['text'];new=changes[k]
            if sorted(TOKEN.findall(old))!=sorted(TOKEN.findall(new)):raise ValueError(f'{k}: token mismatch')
            line['text']=new;seen.add(k)
    if seen!=set(changes):raise ValueError('unknown IDs')
    return obj
def main():
    p=argparse.ArgumentParser();sp=p.add_subparsers(dest='action',required=True)
    a=sp.add_parser('validate');a.add_argument('scene')
    a=sp.add_parser('export-renpy');a.add_argument('scene');a.add_argument('output')
    a=sp.add_parser('patch-json');a.add_argument('source');a.add_argument('translations');a.add_argument('output');a.add_argument('--fields',default='text')
    args=p.parse_args()
    if args.action=='validate':
        e,w=validate(read(args.scene));print('Errors:',e,'Warnings:',w);return bool(e)
    if args.action=='export-renpy':value=export(read(args.scene));output=Path(args.output)
    else:
        if args.fields!='text':raise ValueError('only text field allowed')
        if Path(args.source).resolve()==Path(args.output).resolve():raise ValueError('source overwrite forbidden')
        value=json.dumps(patch_json(read(args.source),read(args.translations)),ensure_ascii=False,indent=2)+'\n';output=Path(args.output)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(value,'utf-8');print('Wrote',output)
    return 0
if __name__=='__main__':
    try:sys.exit(main())
    except (ValueError,KeyError,OSError) as e:print('ERROR:',e,file=sys.stderr);sys.exit(1)
