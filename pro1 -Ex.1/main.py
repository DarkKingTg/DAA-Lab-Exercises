import os
import uvicorn
from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager


# 1. Lifespan defined first
@asynccontextmanager
async def lifespan(app: FastAPI):
    host = os.getenv("HOST", "127.0.0.1")
    port = os.getenv("PORT", "8000")
    
    print("\n" + "="*60)
    print(f" 🚀 Success: The server is running at: http://{host}:{port}")
    print("="*60 + "\n")
    yield  
    print("\n 🛑 Server shutting down. Goodbye!\n")

# 2. App initialized exactly once
app = FastAPI(lifespan=lifespan)

# --- Models ---
class SearchRequest(BaseModel):
    array: List[int]
    target: int

class SearchStep(BaseModel):
    low: int
    high: int
    pos: int
    pos_val: int

class SearchResponse(BaseModel):
    found: bool
    index: Optional[int]
    steps: List[SearchStep]
    sorted_array: List[int]  # ADDED: Send the sorted array back to the UI

# --- Core Algorithm ---
def interpolation_search_with_steps(arr: List[int], target: int) -> SearchResponse:
    steps = []
    
    # Sort a copy of the array so we don't mutate the original input directly
    sorted_arr = sorted(arr)
    
    low = 0
    high = len(sorted_arr) - 1

    while low <= high and target >= sorted_arr[low] and target <= sorted_arr[high]:
        # Prevent division by zero
        if sorted_arr[low] == sorted_arr[high]:
            if sorted_arr[low] == target:
                steps.append(SearchStep(low=low, high=high, pos=low, pos_val=sorted_arr[low]))
                return SearchResponse(found=True, index=low, steps=steps, sorted_array=sorted_arr)
            break

        # Interpolation formula
        pos = low + int(((float(high - low) / (sorted_arr[high] - sorted_arr[low])) * (target - sorted_arr[low])))

        # Boundary safety check
        if pos < low or pos > high:
            break

        steps.append(SearchStep(low=low, high=high, pos=pos, pos_val=sorted_arr[pos]))

        if sorted_arr[pos] == target:
            return SearchResponse(found=True, index=pos, steps=steps, sorted_array=sorted_arr)
        
        if sorted_arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return SearchResponse(found=False, index=None, steps=steps, sorted_array=sorted_arr)

# --- Routes ---
@app.post("/api/search", response_model=SearchResponse)
def run_search(data: SearchRequest):
    if not data.array:
        raise HTTPException(status_code=400, detail="Array cannot be empty")
    return interpolation_search_with_steps(data.array, data.target)

@app.get("/")
def get_ui():
    # Use FileResponse for optimized, non-blocking file serving
    html_path = os.path.join("templates", "Index.html")
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail="index.html not found in templates folder")
    return FileResponse(html_path)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)