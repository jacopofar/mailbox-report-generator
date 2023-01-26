import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from mailbox import Message

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
