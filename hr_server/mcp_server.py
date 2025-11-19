from fastmcp import FastMCP
from mcp_tools import data, tool_maker


mcp = FastMCP("HR Server")


@mcp.tool
def greet(name: str) -> str:
    """A simple tool that greets a person by name."""
    return f"Hello, {name}!"


@mcp.tool
def resume_rewrite(resume:str, job_description:str, personal_info="",questions="") -> str:
    """use this tool to rewrite resume making it more appealing to the job description"""
    response = tool_maker(resume, job_description, personal_info).llm_fx(
        list(data.keys())[0]
    )
    return response


@mcp.tool
def cold_mail_info_present(
    resume:str,
    personal_info:str,
    job_description="",questions=""
) -> str:
    """use this tool to write a cold mail to a recruiter when you have personal info about them"""
    response = tool_maker(resume, job_description, personal_info).llm_fx(
        list(data.keys())[1]
    )
    return response


@mcp.tool
def cold_mail_with_no_info(resume:str, job_description="", personal_info="",questions="") -> str:
    """use this tool to write a cold mail to a recruiter when you have no personal info about them"""
    response = tool_maker(resume, job_description, personal_info).llm_fx(
        list(data.keys())[2]
    )
    return response

@mcp.tool
def followup_email(resume:str, questions:str, job_description="", personal_info="") -> str: 
    "use this tool to write a professional follow-up email answering questions related to a resume." 
    response=tool_maker(resume, job_description, personal_info, questions).email_gen(
        list(data.keys())[3]
    )
    return response

@mcp.tool
def linkedin_apply_email(resume:str, job_post:str, job_description="", personal_info="", questions="") -> str:
    "use this tool to write a short professional email (max five lines) applying for a job from a LinkedIn post."
    response = tool_maker(resume, job_description, personal_info, questions, job_post).linkedin_gen(
        list(data.keys())[4]
    )
    return response

if __name__ == "__main__":
    mcp.run(transport="stdio")
