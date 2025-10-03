import streamlit as st
import asyncio
from fastmcp import Client

st.title("MCP Client Tool Selector")

st.write(
    """
This app helps you select and use the appropriate tool based on your input.
Fill in the fields below and the system will decide which tool to use.
"""
)

resume = st.text_area("Paste your resume:")
job_description = st.text_area("Paste the job description (optional):")
personal_info = st.text_area("Enter personal info (optional):")

# Load tool keys from mcp_tools.py (data)

# Use LLM to decide which tool to use
import yaml
from llm import LLM

with open(
    r"C:\Users\jorda\Downloads\projects\mcp\mcp-hr-work\prompts.yaml", "r"
) as file:
    data = yaml.safe_load(file)
tool_keys = list(data.keys())


def llm_decide_tool(resume, job_description, personal_info, tool_keys):
    llm = LLM().llm
    prompt = f"""
You are an expert assistant. Given the following user input fields, decide which tool key from the list should be used. Only return the tool key, nothing else.

Available tool keys: {tool_keys}

Resume: {resume}
Job Description: {job_description}
Personal Info: {personal_info}

Which tool key is the best fit?
"""
    response = llm.invoke(prompt).content.strip()
    for key in tool_keys:
        if key.lower() in response.lower():
            return key
    return None


# Remove pre-selection. Tool will be selected by LLM at execution time.


async def run_mcp_tool_dynamic(tool_key, resume, job_description, personal_info):
    client = Client("http://localhost:8000/mcp")
    async with client:
        tools = await client.list_tools()
        # Find the tool whose docstring or name matches the tool_key
        tool_name = None
        for t in tools:
            # Try to match by docstring or name
            if (
                tool_key.lower() in t["name"].lower()
                or tool_key.lower() in (t.get("doc", "") or "").lower()
            ):
                tool_name = t["name"]
                break
        if not tool_name:
            # fallback: pick first tool with resume in args
            for t in tools:
                if "resume" in t["args"]:
                    tool_name = t["name"]
                    break
        if not tool_name:
            raise Exception("No matching tool found on MCP server.")
        # Build args dynamically
        tool_args = {}
        for arg in tools[[tt["name"] for tt in tools].index(tool_name)]["args"]:
            if arg == "resume":
                tool_args["resume"] = resume
            elif arg == "job_description":
                tool_args["job_description"] = job_description
            elif arg == "personal_info":
                tool_args["personal_info"] = personal_info
        tool = getattr(client, tool_name)
        result = await tool(**tool_args)
        return result


if st.button("Select Tool with LLM"):

    async def select_tool_with_llm():
        client = Client("http://localhost:8000/mcp")
        async with client:
            tools = await client.list_tools()
            tool_keys = [t["name"] for t in tools]
            selected_tool = llm_decide_tool(
                resume, job_description, personal_info, tool_keys
            )
            return selected_tool

    try:
        selected_tool = asyncio.run(select_tool_with_llm())
        if selected_tool:
            st.success(f"Selected tool: {selected_tool}")
        else:
            st.warning("LLM could not select a tool.")
    except Exception as e:
        st.error(f"Error selecting tool via LLM: {e}")
