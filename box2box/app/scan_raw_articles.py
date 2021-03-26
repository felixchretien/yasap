import json
import os


def get_articles_elements(file):
    with open(file, 'r') as reader:
        raw = reader.read()
        parts = raw.split('\n\n')
        titre = parts[parts.index('!TITRE')+1]
        resume = parts[parts.index('!RÉSUMÉ')+1]
        bas_de_page = parts[parts.index('!BAS DE PAGE')+1]
        texte = parts[parts.index('!TEXTE')+1:]
        date = parts[parts.index('!DATE')+1]

        return date, titre, resume, bas_de_page, texte


def make_articles_json():

    out = dict()

    for file in os.listdir('textes/articles'):

        date, titre, resume, bas_de_page, texte = get_articles_elements('textes/articles/' + file)
        name = file.split('.')[0]

        nested_dict = dict()

        nested_dict['fichier'] = file
        nested_dict['date'] = date
        nested_dict['titre'] = titre
        nested_dict['description'] = resume
        nested_dict['bas_de_page'] = bas_de_page
        nested_dict['texte'] = texte

        out[name] = nested_dict

    with open('textes/articles.json', 'w') as dumpfile:
        json.dump(out, dumpfile)


if __name__ == '__main__':
    if os.getcwd()[-3:] == 'app':
        os.chdir('../../')

    make_articles_json()
