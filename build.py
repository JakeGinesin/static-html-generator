import os, json, shutil, re
from datetime import date, datetime
today = date.today()

def interpret(out, md):
    f, full, fullfc = False, "", 0
    p, fullp, fullpc = False, "", 0
    for linet in md:
        line = linet
        # line dominators (exclusive)
        # headers
        if (re.search("^```$", line) is not None or f) and not p:
            if f == False:
                fullf, fullfc = "", 0
                f = True
                out.write('        <figure class="highlight" style="margin-top:10px; margin-bottom:10px; padding-top:10px; padding-bottom:10px;"><pre><code class="language-sh" data-lang="sh"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">')
            elif "```" in line:
                f = False
                out.write('</pre></td><td class="code"><pre>')
                fullf+="</pre></td></tr></tbody></table></code></pre></figure>"
                out.write(fullf)
            else:
                fullfc+=1
                fullf+="<span>" + str(line) + "</span>"

        elif re.search("^```[a-zA-Z]+\=$", line) is not None or p: 
            if p == False:
                fullp, fullpc = "", 0
                p = True
                out.write('        <figure class="highlight" style="margin-top:10px; margin-bottom:10px; padding-top:10px; padding-bottom:10px;"><pre><code class="language-sh" data-lang="sh"><table class="rouge-table"><tbody><tr><td class="gutter gl"><pre class="lineno">')
            elif "```" in line:
                p = False
                out.write('</pre></td><td class="code"><pre>')
                fullp+="</pre></td></tr></tbody></table></code></pre></figure>"
                out.write(fullp)
            else:
                fullpc+=1
                out.write(str(fullpc) + "\n")
                fullp+="<span>" + str(line) + "</span>"

        elif re.search("^#", line) is not None:
            out.write("<h2 class='header unselectable'>"+line[line.index(" ")+1:].replace("\n","")+"</h2> \n")
        # empty lines
        elif re.search("^$", line) is not None:
            out.write("<br> \n")
        elif re.search("^``[^`]", line) is not None:
            ## replacing text blocks
            tblocks = re.findall(r"``[^`]+``|^``[^`]+``|``[^`]+``$|^``[^`]+``$", line)
            for match in tblocks:
                text = match[match.index("``")+2:match[match.index("``")+1:].index("``")+1]
                tblock = '<figure class="highlight" style="margin-top:10px; margin-bottom:10px; padding-top:10px; padding-bottom:10px;"><pre><code class="language-text" data-lang="text">'+text+'</code></pre></figure>'
                line = line.replace(match, tblock, 1)
                out.write(line) 
        else: ## typical line replacements (nonexclusive)
            ## replacing lines that begin in "-" with "•"
            if re.search("^-", line) is not None:
                line = line.replace("-","•")

            ## replacing links with a tags
            links = re.findall(r"\[[^\[\]\(\)]+\]\([^\[\]\(\)]+\)", line)
            for match in links:
                text = match[match.index("[")+1:match.index("]")]
                l = match[match.index("(")+1:match.index(")")]
                link = '<a href='+l+' target="__blank">'+text+'</a>'
                line = line.replace(str(match), str(link), 1)

            # replacing italics
            italics = re.findall(r"[^\*]\*[^\*]+\*[^\*]|^\*[^\*]+\*[^\*]|[^\*]\*[^\*]+\*$|^\*[^\*]+\*$", line)
            for match in italics:
                text = match[match.index("*")+1:match[match.index("*")+1:].index("*")+1+match.index("*")]
                tblock = '<span class="italic">'+text+'</span>'
                if match[0] == " " : tblock = " " + tblock
                if match[-1] == " " : tblock+= " "
                line = line.replace(match, str(tblock), 1)

            # replacing bolds
            bolds = re.findall(r"[^\*]\*\*[^\*]+\*\*[^\*]|^\*\*[^\*]+\*\*[^\*]|[^\*]\*\*[^\*]+\*\*$|^\*\*[^\*]+\*\*$", line)
            for match in bolds:
                text = match[match.index("**")+2:match[match.index("**")+1:].index("**")+1+match.index("**")]
                tblock = '<span style="font-weight:600;">'+text+'</span>'
                if match[0] == " " : tblock = " " + tblock
                if match[-1] == " " : tblock+= " "
                line = line.replace(str(match), str(tblock), 1)


            ## replacing block quotes
            blocks = re.findall(r"`[^`]+`|^`[^`]+`|`[^`]+`$|^`[^`]+`$", line)
            for match in blocks:
                text = match[match.index("`")+1:match[match.index("`")+1:].index("`")+1]
                block = '<code class="highlighter-rouge" data-lang="text">'+text+'</code>'
                if match[0] == " " : block = " " + block
                if match[-1] == " " : block+= " "

                line = line.replace(match, block, 1)

            out.write(line + "<br> \n")

        # replace links
try: 
    # clear old dirs
    dirs = ["public/pages/braindump","public/pages/custom/active","public/pages/custom/inactive"]
    for dirv in dirs:
        for f in os.listdir(os.path.join(dirv)):
    	       os.remove(os.path.join(dirv, f))
except:
    print("no dirs needed clearing")

try:
    # clear old files
    to_del = ["public/pages/archive.html","public/pages/index.html","public/pages/braindump.html"]
    for item in to_del:
        try : os.remove(item)
        except : continue
except:
    print("no files")

## html -> markdown

# create folders
if not os.path.exists("public/pages/braindump"): os.mkdir("public/pages/braindump")
if not os.path.exists("public/pages/custom"): os.mkdir("public/pages/custom")
if not os.path.exists("public/pages/custom/active"): os.mkdir("public/pages/custom/active")
if not os.path.exists("public/pages/custom/inactive"): os.mkdir("public/pages/custom/inactive")

# braindump -> content
for file in os.listdir(os.path.join("build/braindump")):
    if file[file.index("."):] == ".html":
        shutil.copyfile(os.path.join("build/braindump/" + file), os.path.join("public/pages/braindump/" + file))
    elif file[file.index("."):] == ".md":
        with open('template_html/individual/ibraindump.html', 'r') as temp, open("build/braindump/" + file, 'r') as md:
            title = file[:file.index(".")]
            ft = ' '.join(map(lambda a: a.capitalize(), title.replace("-"," ").replace("_"," ").split()))
            out = open("public/pages/braindump/" + title + ".html","a")
            for line in temp:
                lt = line
                if "{{Title}}" in lt:
                    lt = lt.replace("{{Title}}", ft)
                    out.write(lt)
                elif "{{Content}}" in lt:
                    interpret(out, md)
                else : out.write(lt)

# create braindump file
with open("template_html/braindump_template.html") as temp:
    out = open("public/pages/braindump.html", "a")
    for line in temp:
        lt = line 
        if "{{data}}" in lt:
            r = ""
            ll = os.listdir("public/pages/braindump")
            ll.sort()
            for file in ll: 
                name = file[:file.index(".")]
                r+= '<a class="ll" href="/braindump/'+name+'">'+name+'</a>'
                r+= '<span> </span>'
            lt = lt.replace("{{data}}", r)
            out.write(lt)
        else : out.write(lt)

# blog -> content

# I use a json file to track certain meta details about posts
f = open('data/archive.json')
adata = json.load(f)

# active raw -> content
for file in os.listdir("build/custom/active"):
    if file[file.index("."):] == ".html":
        shutil.copyfile("build/custom/active/" + file, "public/pages/custom/active/" + file)
        if file not in adata:
            name = file[:file.index(".")]
            adata[file] = {}
            adata[file]["title"] = name.replace("-"," ").replace("_"," ")
            adata[file]["date"] = today.strftime("%m/%d/%Y")
            adata[file]["url"] = name
            adata[file]["active"] = True
    elif file[file.index("."):] == ".md":
        with open('template_html/individual/iarchive.html', 'r') as temp, open("build/custom/active/" + file, 'r') as md:
            name = file[:file.index(".")]
            hname = name + ".html"
            ft = ' '.join(map(lambda a: a.capitalize(), name.replace("-"," ").replace("_"," ").split()))
            if hname not in adata:
                adata[hname] = {}
                adata[hname]["title"] = name.replace("-"," ").replace("_"," ")
                adata[hname]["date"] = today.strftime("%m/%d/%Y")
                adata[hname]["url"] = name
                adata[hname]["active"] = True
            out = open("public/pages/custom/active/" + name + ".html","a")
            for line in temp:
                lt = line
                if "{{Title}}" in lt:
                    lt = lt.replace("{{Title}}", ft)
                    out.write(lt)
                elif "{{Content}}" in lt:
                    interpret(out, md)
                elif "{{Date}}" in lt:
                    i = adata[hname]["date"]
                    lt = lt.replace("{{Date}}", datetime.strptime(i, '%m/%d/%Y').strftime("%B %d, %Y"))
                    out.write(lt)
                else : out.write(lt)

# inactive raw -> content
for file in os.listdir("build/custom/inactive"):
    if file[file.index("."):] == ".html":
        shutil.copyfile("build/custom/inactive/" + file, "public/pages/custom/inactive/" + file)
        if file not in adata:
            name = file[:file.index(".")]
            adata[file] = {}
            adata[file]["title"] = name.replace("-"," ").replace("_"," ")
            adata[file]["date"] = today.strftime("%m/%d/%Y")
            adata[file]["url"] = name
            adata[file]["active"] = False
    elif file[file.index("."):] == ".md":
        with open('template_html/individual/iarchive.html', 'r') as temp, open("build/custom/inactive/" + file, 'r') as md:
            name = file[:file.index(".")]
            hname = name + ".html"
            ft = ' '.join(map(lambda a: a.capitalize(), title.replace("-"," ").replace("_"," ").split()))
            if hname not in adata:
                adata[hname] = {}
                adata[hname]["title"] = name.replace("-"," ").replace("_"," ")
                adata[hname]["date"] = today.strftime("%m/%d/%Y")
                adata[hname]["url"] = name
                adata[hname]["active"] = True
            out = open("public/pages/custom/inactive/" + title + ".html","a")
            for line in temp:
                lt = line
                if "{{Title}}" in lt:
                    lt = lt.replace("{{Title}}", ft)
                    out.write(lt)
                elif "{{Content}}" in lt:
                    interpret(out, md)
                elif "{{Date}}" in lt:
                    lt = lt.replace("{{Date}}", adata[hname]["date"])
                    out.write(lt)
                else : out.write(lt)

with open("data/archive.json", "w") as outfile:
    json.dump(adata, outfile)

# remove files not in directory, remove from json
d = []
for file in adata:
    if not file in os.listdir("public/pages/custom/active") and not file in os.listdir("public/pages/custom/inactive"):
        d.append(file)

for r in d : del adata[r]

with open("data/archive.json", "w") as outfile:
    json.dump(adata, outfile)

f.flush()
f.close()

# create index and blog main files
with open("template_html/index_template.html", "r") as temp:
    out = open("public/pages/index.html", "a")
    for line in temp:
        lt = line
        if "{{Data}}" in lt:
            build = ""
            items = list(filter(lambda a: list(a[1].items())[3][1], list(adata.items())))
            items.sort(key=lambda a: datetime.strptime(list(a[1].items())[1][1], '%m/%d/%Y'), reverse=True)
            for item in items[0:3]:
                l = list(item[1].items())
                t, dte, url, active = l[0][1], l[1][1], l[2][1], l[3][1]
                i = '<li><a href="blog/'+url+'">'+t+'</a><span class="date">'+dte.replace("/","-")+'</span></li>' 
                build+=i
            build+='<li><a href="/blog">More →</a></li>'
            out.write(build)
        else : out.write(lt)

with open("template_html/archive_template.html", "r") as temp:
    out = open("public/pages/archive.html", "a")
    for line in temp:
        lt = line
        if "{{Data}}" in lt:
            build = ""
            items = list(filter(lambda a: list(a[1].items())[3][1], list(adata.items())))
            items.sort(key=lambda a: datetime.strptime(list(a[1].items())[1][1], '%m/%d/%Y'), reverse=True)
            for item in items:
                l = list(item[1].items())
                t, dte, url, active = l[0][1], l[1][1], l[2][1], l[3][1]
                i = '<li><a href="blog/'+url+'">'+t+'</a><span class="date">'+dte.replace("/","-")+'</span></li>' 
                build+=i
            out.write(build)
        else : out.write(lt)
