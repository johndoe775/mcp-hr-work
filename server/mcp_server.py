from fastmcp import FastMCP
from mcp_tools import data, tool_maker


mcp = FastMCP("My MCP Server")


@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"


@mcp.tool
def resume_rewrite(resume, job_description, personal_info=""):
    tool_maker(resume, job_description, personal_info).llm_fx(data.keys()[0])


@mcp.tool
def cold_mail_info_present(
    resume,
    personal_info,
    job_description="",
):
    tool_maker(resume, job_description, personal_info).llm_fx(data.keys()[1])


@mcp.tool
def cold_mail_with_no_info(resume, job_description="", personal_info=""):
    tool_maker(resume, job_description, personal_info).llm_fx(data.keys()[2])


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
