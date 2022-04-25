from locale import D_FMT
from bs4 import BeautifulSoup
import re

def add_suggestions(html):
    soup = BeautifulSoup(html,"html.parser")
    res = []
    print(soup)
    for d in soup.code:
        if '\n' not in d:
            for x in d.find_all("span", {"class": "errortext"}):
                x.extract()
            print(d)
            res.append(d.get_text())
    i = 0
    #print(res)
    flag = 0
    while i < len(res):
        while 'aninhado' in res[i]:
            flag = 1
            res[i] = re.sub(r'\)\{ \/\/aninhado','',res[i])
            res[i] += res[i+1]
            pattern = re.findall(r'(\s+if\()',res[i]).pop()
            #res[i] = re.sub(pattern,' && ',res[i])
            res[i] = res[i].replace(pattern,' && ')
            res.pop(i+1)
            j = i+1
            while not('}' in res[j]):
                res[j] = res[j][1:]
                j += 1
            res.pop(j)

        #print(res[i])    
        i += 1

    if flag == 1:
        html += '''
        <h1>Código (c/sugestões)</h1>
        <pre><code>'''
        for r in res:
            html += '<div class="code">' + r + '</div>\n'
        html += '''
        </code></pre>'''
    return html
    


    