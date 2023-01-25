import re
from collections import Counter
from datetime import date, datetime, timezone
from email.utils import parseaddr, parsedate_to_datetime
from mailbox import Message

import plotly.graph_objects as go

# sometimes the mbox files contain weird date formats
# here some cases either ignored or worked around

# 05-08-2005
DD_MM_YYYY = re.compile(r"\d{2}-\d{2}-\d{4}")
# 2016-08-03 18:21:32.174623604 +0000 UTC
ALMOST_ISO = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d+)? \+0+ UTC")


def parse_mail_date(datestr: str) -> datetime:
    """Parse a date string as a datetime object.

    This handles some quirks found in real mbox files, the RFC regarding the
    date format is not always followed it seems.

    """
    if DD_MM_YYYY.match(datestr):
        raise TypeError(f"Missing time in string {datestr}")
    if ALMOST_ISO.match(datestr):
        return datetime.strptime(datestr[:19], "%Y-%m-%d %H:%M:%S").astimezone(
            timezone.utc
        )
    return parsedate_to_datetime(datestr).astimezone(timezone.utc)


class Processor:
    """Base class for a mail report processor.

    This report generator is designed as a pipeline of processors,
    each processor is created and observes all the messages, then generates
    its own piece of HTML.

    All these snippets are put together with some essential boilerplate to
    form a complete report.
    """

    def process(self, msg: Message) -> None:
        """Process a message, integrating it in the current state.

        Parameters
        ----------
        msg : Message
            A message from a mailbox
        """
        raise NotImplementedError("process method not implemented")

    def report_snippet(self) -> str:
        """Generate the HTML snippet for the specific processor.

        Returns
        -------
        str
            An HTML snippet representing the result of the aggregation
        """
        raise NotImplementedError("report_snippet method not implemented")


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
                x=[h for h in range(24)],
                y=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                z=dow_hour,
            ),
        )
        fig.update_layout(title="Messages by UTC hour and day of the week")
        # reading from top to bottom the days of the weekß
        fig.update_yaxes(autorange="reversed")

        return fig.to_html(full_html=False, include_plotlyjs=False)  # type: ignore


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


class MostFrequentAddresses(Processor):
    """Processor for the most frequent addresses."""

    def __init__(self) -> None:
        self.address_count: Counter[str] = Counter()

    def process(self, msg: Message) -> None:
        if msg["From"] is None or msg["To"] is None:
            return
        # if the string is weird we get an Heade ronject, so by forcing
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


class ReportHeader(Processor):
    """Processor for the report introduction text."""

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.count = 0

    def process(self, msg: Message) -> None:
        self.count += 1

    def report_snippet(self) -> str:
        return f"""
        <section style="padding: 1em;font-family: sans-serif;">
            <h3>Report from {self.filename}</h3>
            <p>Report generated on {datetime.now().date().isoformat()}</p>
            <p>Messages present in the file: {self.count:,.0f}.
            This includes sent messages and spam.<p>
        <section>
        """
