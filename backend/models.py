from pydantic import BaseModel, Field

class ReportSource(BaseModel):
    title:str
    url:str
    
class ResearchReport(BaseModel):
    
    executive_summary: str= Field(
        description="A concise summary answering the user's research question. "
    )
    
    key_finding:list[str] = Field(
        description= "The most important factual findings from the research. "
        
    )
    analysis:str = Field(
        description="Detailed analysis based only on the extracted claims."
    )
    sources:list[ReportSource] = Field(
        description="Source used to support the report"
    )