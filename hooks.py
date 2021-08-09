from aqt import mw

from .html_renderer import Progress, render

def on_deck_browser_will_render_content(deck_browser, content) -> None:
    add_on_config = mw.addonManager.getConfig(__name__)
    deck_name = add_on_config["full_deck_name"]
    if not deck_name:
        return
    deck_id = mw.col.decks.byName(deck_name)["id"]

    # Get the total number of cards remaining.
    total = mw.col.db.all(f"select count(id) from cards where did = {deck_id}")[0][0]
    new_total = mw.col.db.all(f"select count(id) from cards where type = 0 and did = {deck_id}")[0][0]

    # Get level of next card to learn.
    new_card_id = mw.col.db.all(f"select id from cards where type = 0 and did = {deck_id} order by due limit 1")[0][0]
    note_id = mw.col.getCard(new_card_id).nid
    note = mw.col.getNote(note_id)
    field_id = note._fmap["Level"][0]
    level = note.fields[field_id]

    # Get level statistics.
    total_radicals = len(mw.col.find_notes(f"sort_field:{level}_0"))
    new_radicals = len(mw.col.find_notes(f"sort_field:{level}_0 is:new"))

    total_kanji = len(mw.col.find_notes(f"sort_field:{level}_1"))
    new_kanji = len(mw.col.find_notes(f"sort_field:{level}_1 is:new"))

    total_vocabulary = len(mw.col.find_notes(f"sort_field:{level}_2"))
    new_vocabulary = len(mw.col.find_notes(f"sort_field:{level}_2 is:new"))

    html = render(
            Progress(total - new_total, total),
            Progress(total_radicals - new_radicals, total_radicals),
            Progress(total_kanji - new_kanji, total_kanji),
            Progress(total_vocabulary - new_vocabulary, total_vocabulary),
            level)

    content.stats += html
