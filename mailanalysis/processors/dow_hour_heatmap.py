from mailbox import Message

import plotly.graph_objects as go

from mailanalysis.processors import Processor, parse_mail_date


class DowHourHeatmap(Processor):
    """Processor to create a heatmap for day of the week and hour.

    The resulting report snippet shows how many messages there were in a
    specific day of the week and hour, e.g. Tuesday at 15

    The hour is in UTC.
    """

    def __init__(self) -> None:
        self.dow_hour = [[0 for _ in range(24)] for _ in range(7)]

    def process(self, msg: Message) -> None:
        if msg["Date"] is None:
            return
        try:
            msg_date = parse_mail_date(msg["Date"])
        except TypeError:
            print(f'cannot parse date {msg["Date"]}')
            return
        utc_hour = msg_date.time().hour
        dow = msg_date.weekday()
        self.dow_hour[dow][utc_hour] += 1

    def report_snippet(self) -> str:
        dow_hour = self.dow_hour
        fig = go.Figure(
            data=go.Heatmap(
                # trick to hide the extra double label
                hoverlabel=dict(namelength=0),
                hovertemplate="%{y} at %{x}: %{z} messages",
                x=(
                    ["12 AM"]
                    + [f"{h} AM" for h in range(1, 12)]
                    + ["12 PM"]
                    + [f"{h} PM" for h in range(1, 12)]
                ),
                y=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                z=dow_hour,
            ),
        )
        fig.update_layout(title="Messages by UTC hour and day of the week")
        # reading from top to bottom the days of the weekß
        fig.update_yaxes(autorange="reversed")

        return fig.to_html(full_html=False, include_plotlyjs=False)  # type: ignore
