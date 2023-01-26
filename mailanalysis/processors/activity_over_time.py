from datetime import date
from mailbox import Message

import plotly.graph_objects as go

from mailanalysis.processors import Processor, parse_mail_date


class ActivityOverTime(Processor):
    """Processor to create an histogram of activity over time.

    It shows how many mails were exchanged per day over time.
    """

    def __init__(self) -> None:
        self.mail_per_day: dict[date, int] = {}

    def process(self, msg: Message) -> None:
        if msg["Date"] is None:
            return
        try:
            msg_date = parse_mail_date(msg["Date"]).date()
        except TypeError:
            print(f'cannot parse date {msg["Date"]}')
            return
        self.mail_per_day[msg_date] = self.mail_per_day.get(msg_date, 0) + 1

    def report_snippet(self) -> str:
        dates = sorted(self.mail_per_day.keys())
        values = [self.mail_per_day[d] for d in dates]
        fig = go.Figure(
            data=go.Scatter(
                x=dates,
                y=values,
            )
        )
        fig.update_layout(title="Messages by UTC hour and day of the week")
        # reading from top to bottom the days of the weekß
        fig.update_layout(
            title_text="Mail per day",
            xaxis_rangeslider_visible=True,
        )

        return fig.to_html(full_html=False, include_plotlyjs=False)  # type: ignore
