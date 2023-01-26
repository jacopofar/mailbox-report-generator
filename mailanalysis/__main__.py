import argparse
import importlib.resources as pkg_resources
import logging
import webbrowser
from pathlib import Path

import mailanalysis
import mailanalysis.static_assets
from mailanalysis.processors import ReportHeader
from mailanalysis.processors.activity_over_time import ActivityOverTime
from mailanalysis.processors.dow_hour_heatmap import DowHourHeatmap
from mailanalysis.processors.most_frequent_addresses import MostFrequentAddresses

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a report on a Mailbox file content."
    )
    parser.add_argument(
        "mbox_file",
        type=str,
        help="The mailbox (.mbox) file to analyze",
    )
    args = parser.parse_args()
    processors = [
        ReportHeader(args.mbox_file),
        DowHourHeatmap(),
        ActivityOverTime(),
        MostFrequentAddresses(),
    ]
    report_content = mailanalysis.process_mbox(
        args.mbox_file,
        processors,
    )
    header_text = pkg_resources.read_text(
        mailanalysis.static_assets, "html_header.html"
    )
    footer_text = pkg_resources.read_text(
        mailanalysis.static_assets, "html_header.html"
    )
    with open(REPORT_FILE, "w") as f:
        f.write(header_text)
        f.write(report_content)
        f.write(footer_text)
    target = f"file://{Path(REPORT_FILE).absolute()}"
    print(f"Report at {target}")
    webbrowser.open(target)


if __name__ == "__main__":
    main()
