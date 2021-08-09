from collections import namedtuple

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
          padding: 3px 5px;
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
