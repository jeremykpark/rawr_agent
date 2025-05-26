import report_creator as rc
import plotly.express as px

def generate_monthly_report():
    with rc.ReportCreator(
            title="Monthly Report",
            description="A summary of the monthly activities. Generated on the first day of each month.",
            footer="Monthly Report Footer",
            logo="octocat",
            ) as report:
                view = rc.Block(
                    rc.Text("Summary of the month"),
                    rc.Group(
                            rc.Metric(
                            heading="Total Events",
                            value="100",
                            ),
                            rc.Metric(
                            heading="Total Participants",
                            value="500",
                            ),
                    ),
                    rc.Bar(px.data.tips(),
                            x="day",
                            y="total_bill"
                            ),
                    )
    return report, view