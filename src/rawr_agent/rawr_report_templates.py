# This file is from RAWR Agent - https://github.com/jeremykpark/rawr_agent
import logging
import json

from pydantic import Field

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig

logger = logging.getLogger(__name__)


class rawrReportTemplatesFunctionConfig(FunctionBaseConfig, name="rawr_report_templates"):
    """
    A function to generate reports from  data using Report Creator https://report-creator.readthedocs.io/en/latest/
    Which report to generate is determined by the report_type parameter when calling the function.
    The reports are defined in the report_templates directory.
    """
    # Add your custom configuration parameters here
    parameter: str = Field(default="default_value", description="Notional description for this parameter")


@register_function(config_type=rawrReportTemplatesFunctionConfig)
async def rawr_report_templates_function(
    config: rawrReportTemplatesFunctionConfig, builder: Builder
):
    # Implement your function logic here
    async def _response_fn(report_type: str, data: str) -> str:
        # Process the input_message and generate output
        #json_data = json.dumps(json_str)
        
        # Create a report based on the report_type
        match report_type:
            case "instant_report":
                # A report that provides details about new events
                from report_templates.instant_report import generate_instant_report
                report_output = generate_instant_report(data)
                report_output[0].save(report_output[1], "report_exports/report.html")
                
            case "weekly_report" | "monthly_report":
                # A report that provides details about the monthly activities
                from report_templates.monthly_report import generate_monthly_report
                report_output = generate_monthly_report(data)
                report_output[0].save(report_output[1], "report_exports/report.html")

        try:
            report_output
        except Exception as e:
            output_message = "No report generated."
        else:
            output_message = "Your report has been created and saved as 'report.html'."

        return output_message

    try:
        yield FunctionInfo.from_fn(_response_fn, description="A function for providing html formatted templates for reports related to platform events. The only two valid report types are monthly_report and new_event_details")
    except GeneratorExit:
        print("Function exited early!")
    finally:
        print("Cleaning up rawr_event_admin workflow.")