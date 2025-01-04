# Pipeline Dashboard Backend

The backend for the Pipeline Dashboard is built using FastAPI. It provides API endpoints for validating AI pipeline diagrams and ensures that the pipelines are Directed Acyclic Graphs (DAGs).

## Features

- **DAG Validation**: Validates pipeline structures to ensure they are DAGs.
- **Lightweight and Fast**: Built using FastAPI for high performance.

## Installation

### Prerequisites

- Python (v3.9 or later)

### Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd pipeline-dashboard/backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
5. Access the API at [http://localhost:8000](http://localhost:8000).

## API Endpoints

- `POST /validate-pipeline`: Validates if the submitted pipeline is a DAG.

### Example Request

```json
{
  "nodes": [
    {
      "id": "customInput-1",
      "type": "customInput",
      "position": { "x": 223, "y": 128 },
      "data": { "id": "customInput-1", "nodeType": "customInput" },
      "width": 224,
      "height": 199
    },
    {
      "id": "customOutput-1",
      "type": "customOutput",
      "position": { "x": 749, "y": 201 },
      "data": { "id": "customOutput-1", "nodeType": "customOutput" },
      "width": 224,
      "height": 199
    }
  ],
  "edges": [
    {
      "source": "customInput-1",
      "sourceHandle": "customInput-1-value",
      "target": "customOutput-1",
      "targetHandle": "customOutput-1-value",
      "type": "smoothstep",
      "animated": true,
      "markerEnd": { "type": "arrow", "height": "20px", "width": "20px" },
      "id": "reactflow__edge-customInput-1customInput-1-value-customOutput-1customOutput-1-value"
    }
  ]
}
```

### Example Response

#### Valid DAG

```json
{
  "is_dag": true,
  "message": "Graph is a valid DAG",
  "num_nodes": 2,
  "num_edges": 1
}
```

#### Invalid DAG

```json
{
  "is_dag": false,
  "message": "Graph contains at least one cycle",
  "num_nodes": 6,
  "num_edges": 6
}
```

## Contact

For questions or issues, please raise an issue on this [github repository](https://github.com/theathleticnerd/pipeline-dashboard-backend).
