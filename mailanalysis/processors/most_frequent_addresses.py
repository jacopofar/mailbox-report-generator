from collections import Counter
from email.utils import parseaddr
from mailbox import Message

import plotly.graph_objects as go

from mailanalysis.processors import Processor


class MostFrequentAddresses(Processor):
    """Processor for the most frequent addresses.

    To keep the chart readable only the 20 more frequent are shown
    """

    def __init__(self, most_common_n: int = 20) -> None:
        self.address_count: Counter[str] = Counter()
        self.most_common_n = most_common_n

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
        top_addresses = self.address_count.most_common(self.most_common_n)[1:]
        top_addresses.append(
            (
                "(others)",
                sum(
                    v for _, v in self.address_count.most_common()[self.most_common_n :]
                ),
            )
        )
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
