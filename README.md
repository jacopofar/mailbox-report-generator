# Mbox mail analysis
![test status](https://github.com/jacopofar/mailbox-analysis/actions/workflows/test.yaml/badge.svg)
![test status](https://github.com/jacopofar/mailbox-analysis/actions/workflows/lint.yaml/badge.svg)

This is a script that analyzes an **mbox** mail export, such as the one provided by Google Takeout from a Gmail box, and produces a report on the content.

![an heatmap representation of number of mail per day and hour](heatmap.png)
![an interactive chart showing the mail activity per day](timeline.png)

## Current reports

* received mails over hour of the day and day of the week
* mail per day over time
* most active addresses

## Usage

You need an export of your mailbox in *mbox* format (for Gmail you can get it from [Google Takeout](https://takeout.google.com/)).

Install the tool using pip:

    python3 -m pip install mailbox-report-generator

Then run this command:

    generate_mbox_report "/path/to/the/mbox/file.mbox"

a report will be created in the form of an HTML file, and opened with your default browser.

## Extending the report

The report is generated by running every message through a series of `Processors`.
Each Processor implements its own logic to aggregate relevant details and can output the report as an HTML string.

These strings are simply concatenated to generate a static HTML file, two processors output the header and footer of this file.

This structure makes it quite easy to add or remove specific analysis, run automated tests and implement caching.

# Possible future improvements

- [ ] Examine the mail lenght and word usage over time
  - Note that extracting text from mails is very hard, the multipart format and the weird formats used by advertise e-mails make it an extremely unreliable operation.
- [ ] Examine the textual content of the emails with SpaCy, retrieve Named Entities like people and locations (see note on previous point)
- [ ] Find which languages are used in the mail body