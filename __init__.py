from collections import namedtuple

from aqt import gui_hooks, mw

Progress = namedtuple("Progress", ["finished", "total"])

def render(
        overall: Progress,
        radical: Progress,
        kanji: Progress,
        vocabulary: Progress,
        level: int):
    return f"""
        <style>
        #wantan_stats {{
          margin-top: 1em;
        }}
        .wantan_stats_table {{
          text-align: left;
          width: 50%;
        }}
        .wantan_stats_table td {{
          padding: 3px;
        }}
        .wantan_stats_table th {{
          text-align: center;
        }}
        </style>

        <div id="wantan_stats">
            <table class="wantan_stats_table">
              <tr>
                <th colspan=4>Wantan</th>
              </tr>
              <tr>
                <td>Overall</td>
                <td>{overall.finished / overall.total * 100:.0f}%</td>
                <td>{overall.finished} / {overall.total}</td>
                <td><progress max={overall.total} value={overall.finished}></progress></td>
              </tr>
              <tr>
                <th colspan=4>Level {level}</th>
              </tr>
              <tr>
                <td>Radical</td>
                <td>{radical.finished / radical.total * 100:.0f}%</td>
                <td>{radical.finished} / {radical.total}</td>
                <td><progress max={radical.total} value={radical.finished}></progress></td>
              </tr>
              <tr>
                <td>Kanji</td>
                <td>{kanji.finished / kanji.total * 100:.0f}%</td>
                <td>{kanji.finished} / {kanji.total}</td>
                <td><progress max={kanji.total} value={kanji.finished}></progress></td>
              </tr>
              <tr>
                <td>Vocabulary</td>
                <td>{vocabulary.finished / vocabulary.total * 100:.0f}%</td>
                <td>{vocabulary.finished} / {vocabulary.total}</td>
                <td><progress max={vocabulary.total} value={vocabulary.finished}></progress></td>
              </tr>
            </table>
        </div>
        """

def on_deck_browser_will_render_content(deck_browser, content) -> None:
    deck_id = mw.col.decks.byName("Japanese::WaniKani::Wantan")["id"]

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

gui_hooks.deck_browser_will_render_content.append(
        on_deck_browser_will_render_content)
