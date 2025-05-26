# This file is from RAWR Agent - https://github.com/jeremykpark/rawr_agent
import report_creator as rc
import plotly.express as px
import json

# Generate a RAWR instant report using the code below
# made with Report Creator by Daren Ace see documentation here: https://report-creator.readthedocs.io/en/latest/api.html

def generate_instant_report():
    #json_data = [json.loads(item) for item in json_data]
    
    # Create a report with various visualizations and metrics
    with rc.ReportCreator(
            title="New Instant Report",
            description="Custom report that could be triggered by an event",
            footer="test",
            logo="octocat",
            ) as report:
                view = rc.Block(
                    rc.Text("Testing a new instant report with various visualizations and metrics."),
                    rc.Group(
                            rc.Metric(
                            heading="Answer to Life, The Universe, and Everything",
                            value="42",
                            ),
                            rc.Metric(
                            heading="Author",
                            value="Douglas Adams",
                            ),
                    ),
                    rc.Bar(px.data.medals_long(),
                            x="nation",
                            y="count",
                            dimension="medal",
                            label="Bar Chart - Olympic Medals",
                    ),
                    rc.Scatter(
                            px.data.iris(),
                            x="sepal_width",
                            y="sepal_length",
                            dimension="species",
                            marginal="histogram",
                            label="Scatter Plot - Iris",
                    ),
                    rc.Scatter(
                            px.data.iris(),
                            x="sepal_width",
                            y="sepal_length",
                            dimension="species",
                            marginal="histogram",
                            label="Scatter Plot - Iris",
                    ),
                )
    return report, view