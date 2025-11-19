import yaml
from llm import LLM
from langchain.prompts import PromptTemplate


with open(r"C:\Users\jorda\Downloads\my_stuff\projects\mcp-hr-work-main\src\prompts.yaml") as file:
    #yaml_data = yaml.safe_load(f)
    data = yaml.safe_load(file)


class tool_maker:
    def __init__(self, resume:str , job_description: str = None, personal_info: str = None,questions: str = None,job_post: str = None):
        self.resume = resume
        self.job_description = job_description
        self.personal_info = personal_info
        self.questions = questions
        self.data = data
        self.job_post = job_post

    def llm_fx(self, key) -> str:
        f"""{self.data[key]["tool_use_case"]}"""
        input_variables = list(self.data[key]["inputs"].keys())
        template = self.data[key]["prompt"].format(
            resume=self.resume,
            job_description=self.job_description,
            personal_info=self.personal_info,
        )
        prompt_template = PromptTemplate(
            input_variables=input_variables, template=template
        )
        chain = prompt_template | LLM().llm
        response = chain.invoke(self.data[key]["inputs"]).content

        return response
    
    def email_gen(self,key='followup_mail_from_resume') -> str:
        
        f"""{self.data[key]["tool_use_case"]}"""
        
        input_variables = list(self.data[key]["inputs"].keys())
        
        template = self.data[key]["prompt"].format(
            resume=self.resume,
            questions=self.questions
        )
        prompt_template = PromptTemplate(
            input_variables=input_variables, template=template
        )
        chain = prompt_template | LLM().llm
        response = chain.invoke(self.data[key]["inputs"]).content

        return response
    

    def linkedin_gen(self, key='apply_mail_from_linkedin_post') -> str:
        f"""{self.data[key]["tool_use_case"]}"""
        
        input_variables = list(self.data[key]["inputs"].keys())
        
        template = self.data[key]["prompt"].format(
            resume=self.resume,
            job_post=self.job_post
        )
        prompt_template = PromptTemplate(
            input_variables=input_variables, template=template
        )
        chain = prompt_template | LLM().llm
        response = chain.invoke(self.data[key]["inputs"]).content

        return response
