"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""


# def reorder_table(browser: aqt.deckbrowser.DeckBrowser):
#     print(f'Rendering...')
#     file_path = os.path.dirname(os.path.abspath(__file__))
#     with open(os.path.abspath(f'{file_path}/src/drag_handler.js'), encoding='UTF-8') as script:
#         contents = script.read()
#         # browser.web.eval(contents)
from .src import deckbrowser

deckbrowser.build_hooks()
