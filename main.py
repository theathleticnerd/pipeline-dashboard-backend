from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, root_validator
from typing import List, Dict, Optional, Any

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

class Position(BaseModel):
    x: float
    y: float

class NodeData(BaseModel):
    id: str
    nodeType: str

class Node(BaseModel):
    id: str
    type: str
    position: Position
    data: NodeData
    width: int
    height: int
    selected: Optional[bool] = None
    positionAbsolute: Optional[Position] = None
    dragging: Optional[bool] = None

    class Config:
        extra = "allow"

    @root_validator(pre=True)
    def set_optional_fields(cls, values):
        # Set default values for optional fields if they're missing
        if 'selected' not in values:
            values['selected'] = False
        if 'dragging' not in values:
            values['dragging'] = False
        if 'positionAbsolute' not in values:
            values['positionAbsolute'] = values.get('position')
        return values

class MarkerEnd(BaseModel):
    type: str
    height: str
    width: str

class Edge(BaseModel):
    source: str
    sourceHandle: Optional[str] = None
    target: str
    targetHandle: Optional[str] = None
    type: Optional[str] = None
    animated: Optional[bool] = False
    markerEnd: Optional[MarkerEnd] = None
    id: Optional[str] = None

    class Config:
        extra = "allow"

class GraphData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

    class Config:
        extra = "allow"

class ValidationResponse(BaseModel):
    is_dag: bool
    message: str
    num_nodes: int
    num_edges: int

def check_dag(nodes: List[Node], edges: List[Edge]) -> Dict[str, Any]:
    # Create adjacency list representation
    graph = {node.id: [] for node in nodes}
    for edge in edges:
        graph[edge.source].append(edge.target)
    
    visited = set()
    recursion_stack = set()
    
    def has_cycle(node_id: str) -> bool:
        visited.add(node_id)
        recursion_stack.add(node_id)
        
        for neighbor in graph[node_id]:
            if neighbor not in visited:
                if has_cycle(neighbor):
                    return True
            elif neighbor in recursion_stack:
                return True
                
        recursion_stack.remove(node_id)
        return False

    # Verify all edges connect existing nodes
    node_ids = {node.id for node in nodes}
    for edge in edges:
        if edge.source not in node_ids or edge.target not in node_ids:
            return {
                "is_dag": False,
                "message": f"Edge references non-existent node: {edge.source} -> {edge.target}"
            }

    # Check for cycles
    for node in nodes:
        if node.id not in visited:
            if has_cycle(node.id):
                return {
                    "is_dag": False,
                    "message": "Graph contains at least one cycle"
                }
    
    return {
        "is_dag": True,
        "message": "Graph is a valid DAG"
    }
 
@app.post('/pipelines/parse', response_model=ValidationResponse)
async def parse_pipleline(graph_data: GraphData):
    try:
        result = check_dag(graph_data.nodes, graph_data.edges)
        result["num_nodes"]= len(graph_data.nodes)
        result["num_edges"]=len(graph_data.edges)
        return ValidationResponse(**result)
    except Exception as e: 
        raise HTTPException(status_code=400, detail=str(e))
@app.get('/')
def read_root():
    return {'Ping': 'Pongo'}

# @app.get('/pipelines/parse')
# def parse_pipeline(pipeline: str = Form(...)):
#     return {'status': 'parsed'}
