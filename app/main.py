from pathlib import Path
from textwrap import wrap

from bs4 import BeautifulSoup
from pygraphviz import AGraph


__HTML_DIR = '../sources/html'


def parse_html():
    persons = []
    edges = []
    for file in Path(__HTML_DIR).iterdir():
        html_doc = Path(file).read_text()
        soup = BeautifulSoup(html_doc, 'html.parser')
        sth = soup.find('p', class_=['stil-1', 'stil-0'])
        # print(dir(sth))
        # print(sth.text)
        # exit()
        # sth = soup.find('h4')['title']
        pers_id = file.stem
        # pers_id = 'p' + file.stem
        persons.append({'id': pers_id, 'name': f'{wrap(sth.text, 40)}'})
        # persons.append({'id': pers_id, 'name': f'<{sth.text}>'})
        for l in soup.find_all('a'):
            nea = l.get('href')
            if 'chr' in nea:
                edges.append((pers_id, 'p' + nea.split('-')[1].split('.')[0]))

    return persons, edges


def create_graph(persons, edges):
    psg = AGraph(overlap='prism', splines=True)
    # psg.layout(prog="fdp")
    psg.layout()
    for p in persons:
        psg.add_node(p['id'], label=p['name'])
    # psg.add_nodes_from(persons)

    for e in edges:
        psg.add_edge(*e)

    psg.write('psg.gv')
    # psg.draw('psg.png')


if __name__ == '__main__':
    fellows, links = parse_html()
    create_graph(fellows, links)
