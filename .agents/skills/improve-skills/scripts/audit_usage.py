#!/usr/bin/env python3
"""Read-only aggregate usage evidence. Never exports prompt bodies or tool arguments."""
import argparse, collections, datetime, hashlib, json, pathlib, re

def actual_request(text):
    text = re.sub(r'<(skill|environment_context|INSTRUCTIONS|skills_instructions)>[\s\S]*?</\1>', '', text)
    if '## My request:' in text:
        return text.split('## My request:', 1)[1].strip()
    if text.lstrip().startswith(('# AGENTS.md instructions', '<permissions', '<environment_context', '<skill>', '# Chrome tabs:')):
        return ''
    return text.strip()

def analyze(paths, days=30):
    counts = {k:collections.Counter() for k in ('explicit_requests','skill_reads','tool_calls')}
    seen=set(); sessions=set(); malformed=0; requests=0
    cutoff=datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(days=days)
    for path in paths:
        session=str(path)
        for line in pathlib.Path(path).read_text(errors='replace').splitlines():
            try: row=json.loads(line)
            except (ValueError,TypeError): malformed+=1; continue
            p=row.get('payload',{}); typ=row.get('type')
            if typ=='session_meta': session=p.get('id',session);sessions.add(session);continue
            stamp=row.get('timestamp')
            if stamp:
                try:
                    if datetime.datetime.fromisoformat(stamp.replace('Z','+00:00'))<cutoff:continue
                except (ValueError,TypeError): pass
            # Same rollout may be copied between session stores; call IDs deduplicate tools.
            ident=p.get('call_id') or p.get('id') or row.get('uuid')
            key=(session,typ,ident or hashlib.sha256(line.encode()).hexdigest())
            if key in seen:continue
            seen.add(key)
            if typ=='response_item' and p.get('type') in ('function_call','custom_tool_call'):
                name=p.get('name','unknown');counts['tool_calls'][name]+=1
                args=p.get('arguments',p.get('input',''))
                if not isinstance(args,str):args=json.dumps(args)
                # Evidence is a requested file read, not proof the skill ran successfully.
                if re.search(r'\b(cat|sed|read|read_text|Get-Content)\b',args):
                    for skill in set(re.findall(r'/skills/(?:\.system/)?([^/\s\"\']+)/SKILL\.md',args)):
                        counts['skill_reads'][skill]+=1
            content=None
            if typ=='event_msg' and p.get('type')=='user_message':content=p.get('message','')
            elif typ=='response_item' and p.get('type')=='message' and p.get('role')=='user':
                content='\n'.join(c.get('text','') for c in p.get('content',[]) if isinstance(c,dict))
            elif typ=='user' and row.get('message',{}).get('role')=='user':
                c=row['message'].get('content','');content=c if isinstance(c,str) else '\n'.join(x.get('text','') for x in c if isinstance(x,dict))
            if content is not None:
                request=actual_request(content)
                if request:
                    # Deduplicate mirrored user messages within a session, retain only hashes.
                    rk=(session,'request',hashlib.sha256(request.encode()).hexdigest())
                    if rk in seen:continue
                    seen.add(rk);requests+=1
                    for skill in set(re.findall(r'(?<![\w/])\$([a-z][a-z0-9-]+)|<command-name>/([a-z][a-z0-9-]+)</command-name>|^/([a-z][a-z0-9-]+)\b',request)):
                        counts['explicit_requests'][next(x for x in skill if x)]+=1
    return dict(window_days=days,scanned_session_ids=len(sessions),user_requests=requests,malformed_lines=malformed,successful_execution='unknown; inspect tool results and final artifacts',**{k:dict(v.most_common()) for k,v in counts.items()})

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--session-root',action='append');ap.add_argument('--days',type=int,default=30);ns=ap.parse_args()
    roots=ns.session_root or ['~/.codex/sessions','~/.codex/archived_sessions','~/.codex/projects']
    files=set()
    for root in roots:
        p=pathlib.Path(root).expanduser()
        files.update(p.rglob('*.jsonl') if p.is_dir() else [p] if p.is_file() else [])
    print(json.dumps(analyze(sorted(files),ns.days),indent=2))
if __name__=='__main__':main()
