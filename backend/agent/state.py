from typing import TypedDict, List , Dict , Any 

class AgentState(TypedDict, total=False ):
    question: str
    search_queries: List[str]
    search_results: List[Dict[str, Any]]
    fetched_content: List[Dict[str , Any]]
    
    claims: List[Dict[str, Any]]
    is_complete:bool
    
    research_iteration:int 
    max_iteration: int
    
    final_report:Dict[str, Any]
    
    error:str
    