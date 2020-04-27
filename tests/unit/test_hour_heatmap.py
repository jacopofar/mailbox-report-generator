
from mailbox import Message

from mailanalysis.processors import DowHourHeatmap


def test_happy_path():
    p = DowHourHeatmap()
    msg = Message()
    msg.set_payload('Hello world!', 'utf-8')
    msg["Date"] = 'Fri, 9 Jun 2006 12:34:56 -0200'
    p.process(msg)
    generated = p.report_snippet()
    assert '"type": "heatmap"' in generated
    assert '"Mon", "Tue", "Wed"' in generated
    hrs = [0] * 24
    assert generated.count(str(hrs)) == 6
    # element 12 + 2 is 1, because it is UTC
    hrs[14] = 1
    assert str(hrs) in generated


def test_empty_mbox():
    p = DowHourHeatmap()
    generated = p.report_snippet()
    assert '"type": "heatmap"' in generated
    assert '"Mon", "Tue", "Wed"' in generated
    # just ensure it's empty all 7 days of the week
    hrs = [0] * 24
    assert generated.count(str(hrs)) == 7

