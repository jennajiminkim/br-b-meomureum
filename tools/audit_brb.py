from pathlib import Path
import hashlib,json,re,subprocess
root=Path(__file__).resolve().parents[1]
files=[p for folder in ['dist','docs','tools','tests'] for p in (root/folder).rglob('*') if p.is_file()]+[root/'README.md',root/'package.json',root/'vercel.json']+[p for p in [root/'submission.md'] if p.exists()]
textfiles=[p for p in files if p.suffix in ['.js','.mjs','.json','.html','.css','.md','.py','.txt']]
patterns={'private_key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----','github_token':r'gh[pousr]_[A-Za-z0-9]{30,}','api_key':r'sk-[A-Za-z0-9_-]{25,}','aws_access':r'AKIA[A-Z0-9]{16}','jwt':r'eyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+','credential_literal':r'''(?i)(?:password|api[_-]?key|access[_-]?token|secret)\s*[:=]\s*["'][^"'\n]{12,}["']''','email':r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}','korean_phone':r'\b01[016789][- ]?\d{3,4}[- ]?\d{4}\b'}
findings=[]
for p in textfiles:
 if p.name=='audit_brb.py':continue
 for lineno,line in enumerate(p.read_text(errors='replace').splitlines(),1):
  for kind,pat in patterns.items():
   if re.search(pat,line):findings.append({'path':str(p.relative_to(root)),'line':lineno,'kind':kind})
assets=[]
for p in files:
 if p.is_relative_to(root/'dist/assets'):
  assets.append({'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
missing=[]
for p in (root/'dist').glob('*'):
 if p.suffix not in ['.html','.css','.js']:continue
 for ref in re.findall(r'''["'(](\./assets/[^"'\s)]+)''',p.read_text()):
  if '${' not in ref and not (root/'dist'/ref).exists():missing.append({'file':p.name,'path':ref})
for p in (root/'dist/assets').rglob('*.mp3'):
 r=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],capture_output=True)
 if r.returncode:missing.append({'file':str(p.relative_to(root)),'error':'decode-failed'})
result={'scope':'current source files, not external Git history or audio semantic content','text_files':len(textfiles),'asset_files':len(assets),'findings_without_values':findings,'missing_or_decode_errors':missing,'env_files':[str(p.relative_to(root)) for p in root.rglob('.env*') if '.git' not in p.parts],'limitations':['Pattern scan cannot prove absence of all secrets or identify voices/people in field recordings.','No individual clinical data; paper interpretation based on user-supplied summary, not full manuscript review.']}
(root/'docs/evidence/source-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
(root/'docs/evidence/asset-manifest.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
