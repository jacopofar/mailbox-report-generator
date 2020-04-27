
from mailbox import Message

from mailanalysis.processors import ActivityOverTime


def test_happy_path():
    p = ActivityOverTime()
    msg = Message()
    msg.set_payload('Hello world!', 'utf-8')
    msg["Date"] = 'Fri, 9 Jun 2006 12:34:56 -0200'
    p.process(msg)
    generated = p.report_snippet()
    assert '"x": ["2006-06-09"], "y": [1]' in generated
    msg = Message()
    # no payload this time
    msg["Date"] = 'Sun, 13 Jun 2006 12:34:56 -0200'
    p.process(msg)
    generated = p.report_snippet()
    assert '"x": ["2006-06-09", "2006-06-13"], "y": [1, 1]' in generated


def test_empty_mbox():
    p = ActivityOverTime()
    generated = p.report_snippet()
    assert '{"type": "scatter", "x": [], "y": []}' in generated

