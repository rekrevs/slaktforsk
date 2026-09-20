from html.parser import HTMLParser
from pathlib import Path
import hashlib,json
class P(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.t=[]
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.t.append(d.strip())
rows=[]
for n,r,main in [('S-0691-gravar-ebba-alfrida-zingmark.html','R-0d13f1e0e6bc75acbf8426e2','Ebba Alfrida Zingmark'),('S-0691-gravar-oskar-alfred-zingmark.html','R-e7d485f210b9d3a322c3b56f','Oskar Alfred Zingmark')]:
 f=Path('genealogy/media')/n;p=P();p.feed(f.read_text());rows.append({'record':r,'main_subject_literal':main,'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'visible_text_lines':p.t,'scope':'Entire retained person page including the three same-grave cards. Footer/provider contacts are site metadata, not person observation.','source_limits':'Administrative grave register. Shared grave does not prove kinship. Parish-name span is unlabelled in saved HTML: no death location inferred. No current remote-page check claimed.','reading_method':'Direct source HTML extraction, no OCR or handwriting. Names and date labels crosschecked in raw HTML. No difficult decisive glyph requires blind second reading.'})
x={'task':'T-0675','locked_before_model_comparison':True,'records':rows};out=Path('genealogy2/verification/T-0675/root-graves-first-initial.json');out.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');print(hashlib.sha256(out.read_bytes()).hexdigest())
