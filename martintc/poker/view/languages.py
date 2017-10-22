from gettext import translation

from martintc.poker.view.ui import output

OPTS = [
        {'code': '0',  'desc': '(ó_ò)'},
        {'code': 'en', 'desc': 'English'},
        {'code': 'es', 'desc': 'Español'}
]

for idx, option in enumerate(OPTS):
    output('{} {}'.format(idx, option['desc']))


def selectLanguage():
    """
    Handles the selection by the user of the language
    :return: the selected language
    """
    idx_selected = None  # TODO Antes era None. Lenguaje por defecto por comodidad
    while not isinstance(idx_selected, int) or not (0 <= idx_selected < len(OPTS)):
        try:
            idx_selected = int(input('=> : '))
        except ValueError:
            pass

    if idx_selected:
        locale = OPTS[idx_selected]['code']
        lang = translation('poker', '/home/madtyn/PycharmProjects/poker/resources/locale', languages=[locale], fallback=True)
    else:
        lang = None

    return lang
