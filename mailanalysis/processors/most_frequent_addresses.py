from collections import Counter
from email.utils import parseaddr
from mailbox import Message

import plotly.graph_objects as go

from mailanalysis.processors import Processor


class MostFrequentAddresses(Processor):
    """Processor for the most frequent addresses."""

    def __init__(self) -> None:
        self.address_count: Counter[str] = Counter()

    def process(self, msg: Message) -> None:
        if msg["From"] is None or msg["To"] is None:
            return
        # if the string is weird we get an Header object, so by forcing
        # the conversion to str it goes back to a parsable mail address
        from_addr = parseaddr(str(msg["From"]))[1].lower()
        self.address_count.update([from_addr])
        to_addr = parseaddr(str(msg["To"]))[1].lower()
        self.address_count.update([to_addr])

    def report_snippet(self) -> str:
        # ignore address #1 assuming it is the mailbox owner
        top_addresses = self.address_count.most_common(20)[1:]
        labels, values = zip(*top_addresses)
        fig = go.Figure(
            data=go.Pie(
                values=values,
                labels=labels,
            )
        )
        # reading from top to bottom the days of the weekß
        fig.update_layout(
            title_text="Most active addresses",
        )

        return fig.to_html(full_html=False, include_plotlyjs=False)  # type: ignore
