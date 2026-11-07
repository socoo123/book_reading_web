"""Minimal byte/compatibility and MD/HTML checks. Local authoring dependencies only."""
from pathlib import Path
from io import BytesIO
from html.parser import HTMLParser
import base64
import copy
import json
import re
import sys
import xml.etree.ElementTree as ET

TOOLS = Path('/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools')
sys.path.insert(0, str(TOOLS / 'ch05-python'))
import markdown
import msgpack
import fastavro
import jsonschema
import google.protobuf
from google.protobuf import descriptor_pb2, descriptor_pool, message_factory, json_format

BOOK = Path(__file__).resolve().parents[2]
results = {}
record = {'userName':'Martin','favoriteNumber':1337,'interests':['daydreaming','hacking']}
json_bytes = json.dumps(record,separators=(',',':')).encode()
mp = msgpack.packb(record,use_bin_type=True)
assert len(json_bytes)==81 and len(mp)==66
assert mp[:2]==bytes.fromhex('83 a8') and bytes.fromhex('cd 05 39') in mp
assert msgpack.packb('a'*24)[0] == 0xb8
assert len(base64.b64encode(b'a'*300))==400 and len(base64.b64encode(b'a'))==4

def person(extra=False, number_type=3):
    f = descriptor_pb2.FileDescriptorProto(name='person.proto',syntax='proto3')
    m = f.message_type.add(name='Person')
    for name,num,kind,label in [('user_name',1,9,1),('favorite_number',2,number_type,1),('interests',3,9,3)]+([('email',4,9,1)] if extra else []):
        m.field.add(name=name,number=num,type=kind,label=label)
    p = descriptor_pool.DescriptorPool()
    p.Add(f)
    return message_factory.GetMessageClass(p.FindMessageTypeByName('Person'))

Old,New = person(),person(True)
pb = Old(user_name='Martin',favorite_number=1337,interests=record['interests']).SerializeToString()
expected = b'\x0a\x06Martin\x10\xb9\x0a\x1a\x0bdaydreaming\x1a\x07hacking'
assert pb==expected and len(pb)==33
assert len(Old(favorite_number=-1).SerializeToString())==11 # one-byte tag + ten-byte value
assert person(number_type=18)(favorite_number=-1).SerializeToString()==bytes.fromhex('10 01')
assert New.FromString(pb).email=='' # backward: new reader, old data
old = Old.FromString(New(user_name='Martin',email='m@example.test').SerializeToString())
old.favorite_number=42
assert New.FromString(old.SerializeToString()).email=='m@example.test' # forward & writeback
old_json = json_format.MessageToJson(old)
reconstructed = Old()
json_format.Parse(old_json,reconstructed)
assert New.FromString(reconstructed.SerializeToString()).email=='' # binary -> JSON loses unknowns
assert person(number_type=5).FromString(Old(favorite_number=4294967297).SerializeToString()).favorite_number==1

schema = {'type':'record','name':'Person','fields':[
    {'name':'userName','type':'string'},
    {'name':'favoriteNumber','type':['null','long'],'default':None},
    {'name':'interests','type':{'type':'array','items':'string'}}]}
def avro_bytes(data,s):
    output=BytesIO()
    fastavro.schemaless_writer(output,s,data)
    return output.getvalue()
av=avro_bytes(record,schema)
assert av==b'\x0cMartin\x02\xf2\x14\x04\x16daydreaming\x0ehacking\x00' and len(av)==32
reader=copy.deepcopy(schema)
reader['fields'] = [reader['fields'][1],reader['fields'][0],{'name':'locale','type':'string','default':'zh-CN'}]
projection=fastavro.schemaless_reader(BytesIO(av),schema,reader)
assert projection=={'favoriteNumber':1337,'userName':'Martin','locale':'zh-CN'}
# The output dict order is not the encoded writer order; explicit reader encoding follows the reader schema.
assert 'interests' not in projection
without_default=copy.deepcopy(reader)
del without_default['fields'][2]['default']
def rejects(reader):
    try: fastavro.schemaless_reader(BytesIO(av),schema,reader)
    except fastavro._read_common.SchemaResolutionError: return True
    return False
assert rejects(without_default)
narrow=copy.deepcopy(schema)
narrow['fields'][1]['type']=['null','int']
assert rejects(narrow) # Figure 5-6 long -> int is not supported even though 1337 fits
old_schema={'type':'record','name':'User','fields':[{'name':'userName','type':'string'}]}
new_schema=copy.deepcopy(old_schema)
new_schema['fields'].append({'name':'email','type':['null','string'],'default':None})
assert fastavro.schemaless_reader(BytesIO(avro_bytes({'userName':'Martin'},old_schema)),old_schema,new_schema)['email'] is None
assert fastavro.schemaless_reader(BytesIO(avro_bytes({'userName':'Martin','email':'x'},new_schema)),new_schema,old_schema)=={'userName':'Martin'}
shape={'type':'object','patternProperties':{'^[0-9]+$':{'type':'string'}},'additionalProperties':False}
v=jsonschema.Draft7Validator(shape)
assert v.is_valid({'42':'Martin'}) and v.is_valid({'042':'Martin'})
assert not v.is_valid({'name':'Martin'}) and not v.is_valid({'42':7})
results['bytes']={k:len(v) for k,v in [('json',json_bytes),('messagepack',mp),('protobuf',pb),('avro',av)]}
results['compatibility']='Protobuf binary/JSON unknown fields, default, int truncation; Avro default, projection, unsupported narrowing; JSON Schema key/value examples passed'
results['versions']={'protobuf':google.protobuf.__version__,'msgpack':msgpack.__version__,'fastavro':fastavro.__version__,'jsonschema':'4.25.1'}

md=(BOOK/'notes/ch05.md').read_text()
page=(BOOK/'chapters/ch05.html').read_text()
class Text(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self,data): self.parts.append(data)
def plain(value):
    p=Text();p.feed(value)
    return re.sub(r'\s+','',''.join(p.parts))
body=md.split('<details id="sources"')[0]
sections=re.findall(r'<a id="([^"]+)"></a>\s*## (\d+)　([^\n]+)\n(.*?)(?=<a id="|\Z)',body,re.S)
for anchor,number,title,content in sections:
    actual=re.search(rf'<section id="{anchor}">(.*?)</section>',page,re.S).group(1)
    expected=markdown.markdown(f'## {number}{title}\n\n{content}',extensions=['fenced_code','tables'])
    assert plain(expected)==plain(actual),anchor
source_md=md.split('<summary>来源、原书对应与核查说明</summary>')[1].split('</details>')[0]
source_html=page.split('<summary>来源、原书对应与核查说明</summary>')[1].split('</details>')[0]
assert plain(markdown.markdown(source_md,extensions=['fenced_code','tables']))==plain(source_html)
intro=md.split('<a id="compatibility">')[0].splitlines()[4:]
intro_html=re.search(r'<p>给用户资料.*?(?=<details class="mobile-toc">)',page,re.S).group()
assert plain(markdown.markdown('\n'.join(intro)))==plain(intro_html)
assert len(sections)==15 and page.count('<figure ')==3
assert not re.search(r'(?:href|src)="[^"]*/(?:notes|sources|originals)/',page)
elements=0
for stem in ['compatibility','avro-resolution','durable-boundary']:
    scene=json.loads((BOOK/f'diagrams/sources/ch05-{stem}.excalidraw').read_text())
    svg=ET.parse(BOOK/f'diagrams/exports/ch05-{stem}.svg').getroot()
    exported=''.join(svg.itertext())
    for e in scene['elements']:
        if e['type']=='text':
            assert re.sub(r'\s+','',e['text']) in re.sub(r'\s+','',exported),(stem,e['text'])
    assert not any(e['type']=='image' for e in scene['elements'])
    elements+=len(scene['elements'])
results['content']={'sections':15,'figures':3,'nativeElements':elements,'mdHtml':'all sections, intro, sources match'}
(TOOLS/'ch05-check-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
