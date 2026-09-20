import pathlib,subprocess,json
b=pathlib.Path(__file__).resolve().parent
for task in ['x','y','z']:
 for p in (b/'blind'/task).glob('*.json'):
  dest=b/'scores'/f'{p.stem}.auto.json';dest.parent.mkdir(exist_ok=True)
  if dest.exists():continue
  cmd=['python',str(b/('score_'+task+'.py')),str(p)] if task in ['x','y'] else ['node',str(b/'z/private/evaluate.mjs'),str(p)]
  r=subprocess.run(cmd,capture_output=True,text=True)
  try:d=json.loads(r.stdout)
  except Exception:d={'error':r.stderr or r.stdout,'process_exit':r.returncode}
  dest.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Automatic scored',len(list((b/'scores').glob('*.auto.json'))))
