import argparse

import mailanalysis
from mailanalysis.processors import (
    ActivityOverTime,
    DowHourHeatmap,
    MostFrequentAddresses,
)


def main():

    parser = argparse.ArgumentParser(
        description='Generate a report on a Mailbox file content.'
    )
    parser.add_argument(
        'mbox_file',
        type=str,
        help='The mailbox (.mbox) file to analyze',
    )
    args = parser.parse_args()
    processors = [
        DowHourHeatmap(),
        ActivityOverTime(),
        MostFrequentAddresses()
    ]
    report_content = mailanalysis.process_mbox(
        args.mbox_file,
        processors,
    )

    with open('report.html', 'w') as f:
        # mega ugly :) but enough to see the result an iterate
        f.write('''
        <html>
<head><meta charset="utf-8" /></head>
<body>
    <div>

    <script type="text/javascript">
        window.PlotlyConfig = {MathJaxConfig: 'local'};
    </script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        ''')
        f.write(report_content)
        f.write('</body></html>')


if __name__ == "__main__":
    main()
