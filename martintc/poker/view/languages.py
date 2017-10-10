from gettext import translation

from martintc.poker.view.ui import output

OPTS = [
        {'code':'0',  'desc':'(ó_ò)'},
        {'code':'en', 'desc':'English'},
        {'code':'es', 'desc':'Español'}
        ]

for idx, option in enumerate(OPTS):
    output('{} {}'.format(idx, option['desc']))

def selectLanguage():
    idxSelected = None  # TODO Antes era None. Lenguaje por defecto por comodidad
    while not isinstance(idxSelected, int) or not (0 <= idxSelected < len(OPTS)):
        try:
            idxSelected = int(input('=> : '))
        except ValueError:
            pass

    if idxSelected:
        locale = OPTS[idxSelected]['code']
        lang = translation('poker', '/home/madtyn/PycharmProjects/poker/resources/locale', languages=[locale], fallback=True)
    else:
        lang=None

    return lang
