import os
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain_neo4j import Neo4jGraph
from langchain.chains import GraphCypherQAChain
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="TransitGuard Knowledge Graph API")

# Initialize Neo4j connection
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    username=os.getenv("NEO4J_USERNAME", "neo4j"),
    password=os.getenv("NEO4J_PASSWORD", "password")
)

# Initialize Ollama LLM
llm = Ollama(model="llama2")

# Create GraphCypherQAChain
chain = GraphCypherQAChain.from_llm(
    graph=graph,
    llm=llm,
    verbose=True,
    allow_dangerous_requests=True
)

class Query(BaseModel):
    question: str

def load_safety_data():
    """Load safety index data into Neo4j"""
    try:
        # Read CSV file
        df = pd.read_csv('data/safety_index.csv')
        
        # Create nodes and relationships
        for _, row in df.iterrows():
            # Create SafetyIndex node
            query = """
            MERGE (s:SafetyIndex {date: $date})
            SET s.score = $score
            """
            graph.query(query, {
                "date": row['Date'],
                "score": float(row['safety_index'])
            })
            
            # Create relationships between consecutive days
            if _ > 0:
                prev_date = df.iloc[_ - 1]['Date']
                query = """
                MATCH (prev:SafetyIndex {date: $prev_date})
                MATCH (curr:SafetyIndex {date: $curr_date})
                MERGE (prev)-[:NEXT_DAY]->(curr)
                """
                graph.query(query, {
                    "prev_date": prev_date,
                    "curr_date": row['Date']
                })
        
        return True
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return False

@app.on_event("startup")
async def startup_event():
    """Initialize the knowledge graph on startup"""
    if not load_safety_data():
        raise HTTPException(status_code=500, detail="Failed to initialize knowledge graph")

@app.post("/query")
async def query_graph(query: Query) -> Dict[str, Any]:
    """Query the knowledge graph with a natural language question"""
    try:
        response = chain.invoke({"query": query.question})
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/schema")
async def get_schema() -> Dict[str, Any]:
    """Get the current graph schema"""
    try:
        return {"schema": graph.schema}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 