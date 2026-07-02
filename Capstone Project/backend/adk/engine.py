import time
from typing import Dict, Any, List, Callable

class WorkflowState:
    """
    Shared context/state holding the market data, technical analyses, 
    sentiment reports, and final briefs.
    """
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.logs: List[str] = []
        
    def set(self, key: str, value: Any):
        self.data[key] = value
        
    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)
        
    def log(self, message: str):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append(f"[{timestamp}] {message}")

class WorkflowNode:
    """Represents a single agent step inside the workflow graph"""
    def __init__(self, name: str, action_func: Callable[[WorkflowState], None]):
        self.name = name
        self.action = action_func
        
    def execute(self, state: WorkflowState) -> float:
        state.log(f"Starting execution of Node: '{self.name}'")
        start_time = time.time()
        try:
            self.action(state)
            duration = time.time() - start_time
            state.log(f"Completed Node: '{self.name}' in {duration:.4f}s")
            return duration
        except Exception as e:
            state.log(f"Error in Node: '{self.name}' - {str(e)}")
            raise

class WorkflowGraph:
    """
    ADK 2.0 Graph Workflow runner that registers nodes, 
    manages execution flow, and outputs results.
    """
    def __init__(self):
        self.nodes: Dict[str, WorkflowNode] = {}
        self.edges: List[tuple] = []  # pairs of (from_node, to_node)
        self.execution_order: List[str] = []
        
    def add_node(self, name: str, action_func: Callable[[WorkflowState], None]):
        self.nodes[name] = WorkflowNode(name, action_func)
        
    def add_edge(self, from_node: str, to_node: str):
        if from_node not in self.nodes or to_node not in self.nodes:
            raise ValueError(f"Nodes must exist before creating edges: {from_node} -> {to_node}")
        self.edges.append((from_node, to_node))
        
    def set_execution_order(self, order: List[str]):
        """Sets sequential or topological execution order manually for deterministic flows"""
        for node in order:
            if node not in self.nodes:
                raise ValueError(f"Node '{node}' is not registered in this graph")
        self.execution_order = order
        
    def run(self, initial_state: WorkflowState = None) -> WorkflowState:
        state = initial_state or WorkflowState()
        state.log("Initializing Graph Workflow Execution...")
        
        # If execution order is not set, resolve using dependencies or simple sequence
        order = self.execution_order if self.execution_order else list(self.nodes.keys())
        
        performance = {}
        state.set("performance", performance)
        
        for node_name in order:
            node = self.nodes[node_name]
            duration = node.execute(state)
            performance[node_name] = duration
            
        state.log("Graph Workflow Execution Completed Successfully.")
        return state
