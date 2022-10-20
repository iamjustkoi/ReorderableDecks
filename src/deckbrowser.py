"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""

import aqt.deckbrowser
from aqt import gui_hooks, mw

default_row_count = 2


def build_hooks():
    gui_hooks.deck_browser_did_render.append(reorder_table)
    gui_hooks.deck_browser_did_render.append(append_input_handler)


def append_input_handler(browser: aqt.deckbrowser.DeckBrowser):

    pass


def deck_list(deck_keys: [int]):
    conf = mw.addonManager.getConfig(__name__)

    # Place dids in ordered list
    ordered_dids = []
    for did, pos in conf.items():
        ordered_dids.insert(pos, did) if did in deck_keys else None

    # Handle unrecognized values
    if deck_keys != list(conf.keys()):

        for did in deck_keys:
            # Place at bottom
            ordered_dids.append(did) if did not in ordered_dids else None

        conf.clear()
        for did in ordered_dids:
            conf[did] = len(conf)

        mw.addonManager.writeConfig(__name__, conf)

    return ordered_dids


def reorder_table(browser: aqt.deckbrowser.DeckBrowser):
    deck_keys = [str(name_id.id) for name_id in browser.mw.col.decks.all_names_and_ids(skip_empty_default=True)]
    deck_map = deck_list(deck_keys)

    def remove_children(children):
        for child in children:
            if child.children:
                remove_children(child.children)
            # remove node
            deck_map.remove(str(child.deck_id))

    def update_from_node(node):
        for child in node.children:
            if child.children:
                if not child.collapsed:
                    update_from_node(child)
                else:
                    remove_children(child.children)

    top = browser.mw.col.sched.deck_due_tree()
    update_from_node(top)

    for did in deck_map:
        pos = deck_map.index(did)
        js = f'''
            {{
                let curr_row = document.getElementById("{did}");
                
                if (typeof index_row !== undefined) {{
                    let index_row = document.querySelectorAll(`table tr`)[{int(pos) + default_row_count}];
                    
                    if (typeof index_row !== undefined) {{
                        console.log(`Swapping: {did}->${{index_row.id}}`);
                        curr_row.parentElement.insertBefore(curr_row, index_row);
                    }}
                }}
            }}
        '''
        browser.web.eval(js)

    # for did in deck_keys:
    #     # if ke in deck_map.values():
    #         pos = stored_did_ords.get(str(did))
    #         # Find tr where id={did}
