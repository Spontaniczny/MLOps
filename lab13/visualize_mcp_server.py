from fastmcp import FastMCP
from typing import Annotated
import matplotlib.pyplot as plt
import io
import base64

mcp = FastMCP("Make plots using matplotlib")


@mcp.tool(description='Make plot using matplotlib. Return plot encoded in base64.')
def get_current_datetime(
    data: Annotated[list[list[float]], "Points that we want to plot"],
    title: Annotated[str, "Title of the plot"] = "",
    x_label: Annotated[str, "Name of x axis."] = "X",
    y_label: Annotated[str, "Name of y axis."] = "Y",
    legend: Annotated[bool, "Do we want to display the legend"] = False,
) -> str:
    fig, ax = plt.subplots()

    for i, series in enumerate(data):
        ax.plot(series, label=f"Series {i + 1}")

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    if legend and len(data) > 0:
        ax.legend()

    buffer = io.BytesIO()

    plt.savefig(buffer, format='png')
    plt.close(fig)

    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')

    return img_str


mcp.run(transport="streamable-http", port=8003)
