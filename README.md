# TransitGuard Knowledge Graph API

A knowledge graph-based API for analyzing and querying transit safety data, powered by Neo4j and Ollama. This system processes daily safety index data and provides natural language querying capabilities.

## Features

- **Knowledge Graph Storage**: Stores safety index data in Neo4j graph database
- **Natural Language Queries**: Ask questions about safety data in plain English
- **Temporal Analysis**: Track safety trends over time
- **REST API**: Easy integration with other applications
- **Docker Support**: Containerized deployment

## System Architecture

- **Backend**: FastAPI application
- **Database**: Neo4j graph database
- **LLM**: Ollama with llama2 model
- **Containerization**: Docker and Docker Compose

## Prerequisites

1. Docker and Docker Compose
   - Install Docker from https://docs.docker.com/get-docker/
   - Install Docker Compose from https://docs.docker.com/compose/install/

2. Ollama
   - Install Ollama from https://ollama.ai/
   - Pull the llama2 model: `ollama pull llama2`

## Setup

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd TransitGuardRAG_v2
```

2. Build and start the containers:
```bash
docker-compose up --build
```

The services will be available at:
- API: http://localhost:8000
- Neo4j Browser: http://localhost:7474 (username: neo4j, password: password)

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your Neo4j credentials:
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password
```

3. Run the application:
```bash
python app.py
```

## API Documentation

### Endpoints

#### POST /query
Query the knowledge graph with natural language questions.

Request:
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "What was the safety index on January 1st, 2024?"}'
```

Response:
```json
{
    "answer": "The safety index on January 1st, 2024 was 66.0"
}
```

#### GET /schema
Get the current graph schema.

Request:
```bash
curl "http://localhost:8000/schema"
```

Response:
```json
{
    "schema": {
        "nodes": ["SafetyIndex"],
        "relationships": ["NEXT_DAY"],
        "properties": {
            "SafetyIndex": {
                "date": "STRING",
                "score": "FLOAT"
            }
        }
    }
}
```

## Data Structure

### Graph Schema

The knowledge graph contains:

1. **Nodes**:
   - `SafetyIndex`
     - Properties:
       - `date`: The date of the safety index (STRING)
       - `score`: The safety index score (FLOAT)

2. **Relationships**:
   - `NEXT_DAY`: Connects consecutive days
     - From: SafetyIndex node
     - To: SafetyIndex node

### Example Data Flow

1. CSV data is loaded into Neo4j on application startup
2. Each row creates a SafetyIndex node
3. Consecutive days are connected via NEXT_DAY relationships
4. The graph structure enables temporal queries and trend analysis

## Query Examples

You can ask questions like:

1. **Specific Date Queries**:
   - "What was the safety index on January 1st, 2024?"
   - "What was the safety score for December 25th, 2023?"

2. **Trend Analysis**:
   - "What was the trend in safety index over the last week?"
   - "How has the safety index changed in the last month?"

3. **Statistical Queries**:
   - "What was the highest safety index recorded?"
   - "What was the average safety index for January 2024?"
   - "What was the lowest safety score in December 2023?"

4. **Comparative Analysis**:
   - "Compare the safety indices between January and February 2024"
   - "What was the difference in safety scores between weekdays and weekends?"

## Docker Commands

- Start the services: `docker-compose up`
- Start in detached mode: `docker-compose up -d`
- Stop the services: `docker-compose down`
- View logs: `docker-compose logs -f`
- Rebuild containers: `docker-compose up --build`
- Remove volumes: `docker-compose down -v`

## Development

### Project Structure
```
TransitGuardRAG_v2/
├── app.py              # FastAPI application
├── data/              # Data directory
│   └── safety_index.csv
├── Dockerfile         # Application container definition
├── docker-compose.yml # Multi-container setup
├── requirements.txt   # Python dependencies
└── README.md         # Documentation
```

### Adding New Features

1. **New Data Sources**:
   - Add CSV files to the `data/` directory
   - Update the `load_safety_data()` function in `app.py`

2. **New Query Types**:
   - The system automatically handles new query types through the LLM
   - No code changes required for new natural language queries

## Troubleshooting

1. **Neo4j Connection Issues**:
   - Check if Neo4j is running: `docker-compose ps`
   - Verify credentials in `.env` file
   - Check Neo4j logs: `docker-compose logs neo4j`

2. **API Issues**:
   - Check application logs: `docker-compose logs app`
   - Verify Ollama is running: `ollama list`
   - Ensure llama2 model is pulled: `ollama pull llama2`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here] 