import json
d=json.load(open('channels.json'))
drop={'Pluto TV Documentaries','BBC Food','BBC Home','WeatherNation','CBC News Network','PBS Nature','PBS Travel'}
d['channels']=[c for c in d['channels'] if c['name'] not in drop]
json.dump(d,open('channels.json','w'),indent=2,ensure_ascii=False)
rows=[]
for c in d['categories']:
    n=[x['name'] for x in d['channels'] if x['category']==c['id']]
    rows.append("### %s (%d)\n%s  \nPlaylist: categories/%s.m3u\n\n%s\n" % (c['title'],len(n),c['description'],c['id'],", ".join(n)))
open('CATEGORIES.md','w').write("# Categories\n\nGenerated from channels.json. Each category is also its own playlist.\n\n"+"\n".join(rows))
print(len(d['channels']))
