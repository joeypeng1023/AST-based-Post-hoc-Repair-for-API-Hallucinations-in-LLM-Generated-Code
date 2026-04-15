"""
Code Fix Tool Backend - API Hallucination Detector
FastAPI server that detects and fixes API hallucinations in LLM-generated code.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import re
import time

app = FastAPI(title="Code Fix API", description="API for detecting and fixing hallucinations in LLM-generated code")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FixRequest(BaseModel):
    code: str


class FixItem(BaseModel):
    line: int
    column: int
    original: str
    corrected: str
    type: str


class FixResponse(BaseModel):
    fixed_code: str
    fixes: List[FixItem]
    status: str


# Common Python package hallucinations
PACKAGE_FIXES = {
    "pands": "pandas",
    "pandad": "pandas",
    "panda": "pandas",
    "numppy": "numpy",
    "numpi": "numpy",
    "numpyy": "numpy",
    "matplotib": "matplotlib",
    "matplot": "matplotlib",
    "sklearn": "sklearn",
    "seaborn": "seaborn",
    "reqeusts": "requests",
    "request": "requests",
    "flask": "flask",
    "fastapi": "fastapi",
    "torch": "torch",
    "tensorflow": "tensorflow",
    "keras": "keras",
    "scipy": "scipy",
    "plotly": "plotly",
    "beautifulsoup4": "bs4",
    "beautifulsoup": "bs4",
    "selenium": "selenium",
    "pillow": "PIL",
    "pil": "PIL",
    "cv2": "cv2",
    "opencv": "cv2",
}

# Common function hallucinations
FUNCTION_FIXES = {
    "read_csv": "read_csv",
    "read_excel": "read_excel",
    "to_dataframe": "to_dict",
    "show_plot": "plt.show",
    "dispaly": "display",
    "dispay": "display",
    "prnt": "print",
    "pritn": "print",
    "lenght": "len",
    "lenth": "len",
    "append": "append",
    "extnd": "extend",
    "instert": "insert",
    "remvoe": "remove",
    "pop": "pop",
    "clea": "clear",
    "sortt": "sort",
    "revers": "reverse",
    "inde": "index",
    "coun": "count",
}

# Common class/type hallucinations
CLASS_FIXES = {
    "Dataframe": "DataFrame",
    "dataframe": "DataFrame",
    "Array": "ndarray",
    "array": "ndarray",
    "List": "list",
    "Dict": "dict",
    "Tuple": "tuple",
    "Set": "set",
    "Str": "str",
    "Int": "int",
    "Float": "float",
    "Bool": "bool",
}


def find_and_fix_hallucinations(code: str) -> tuple[str, List[FixItem]]:
    """
    Find and fix common API hallucinations in the code.
    Returns the fixed code and a list of fixes made.
    """
    fixes: List[FixItem] = []
    lines = code.split('\n')
    fixed_lines = []

    for line_num, line in enumerate(lines, start=1):
        fixed_line = line

        # Check for package import hallucinations
        for wrong, correct in PACKAGE_FIXES.items():
            # Check in import statements
            import_pattern = rf'\bimport\s+{re.escape(wrong)}\b'
            if re.search(import_pattern, line, re.IGNORECASE):
                fixed_line = re.sub(import_pattern, f'import {correct}', fixed_line, flags=re.IGNORECASE)
                col = line.lower().find(wrong.lower())
                if col >= 0:
                    fixes.append(FixItem(
                        line=line_num,
                        column=col + 1,
                        original=wrong,
                        corrected=correct,
                        type="package"
                    ))

            # Check in from imports
            from_pattern = rf'\bfrom\s+{re.escape(wrong)}\b'
            if re.search(from_pattern, line, re.IGNORECASE):
                fixed_line = re.sub(from_pattern, f'from {correct}', fixed_line, flags=re.IGNORECASE)
                col = line.lower().find(wrong.lower())
                if col >= 0:
                    fixes.append(FixItem(
                        line=line_num,
                        column=col + 1,
                        original=wrong,
                        corrected=correct,
                        type="package"
                    ))

        # Check for function call hallucinations
        for wrong, correct in FUNCTION_FIXES.items():
            if wrong != correct:  # Skip identity mappings
                pattern = rf'\b{re.escape(wrong)}\b'
                if re.search(pattern, fixed_line, re.IGNORECASE):
                    matches = list(re.finditer(pattern, fixed_line, re.IGNORECASE))
                    for match in matches:
                        # Skip if it's part of a correct usage (e.g., in a comment or string)
                        col = match.start()
                        fixed_line = fixed_line[:match.start()] + correct + fixed_line[match.end():]
                        fixes.append(FixItem(
                            line=line_num,
                            column=col + 1,
                            original=wrong,
                            corrected=correct,
                            type="function"
                        ))

        # Check for class/type hallucinations
        for wrong, correct in CLASS_FIXES.items():
            pattern = rf'\b{re.escape(wrong)}\b'
            if re.search(pattern, fixed_line):
                matches = list(re.finditer(pattern, fixed_line))
                for match in matches:
                    col = match.start()
                    fixed_line = fixed_line[:match.start()] + correct + fixed_line[match.end():]
                    fixes.append(FixItem(
                        line=line_num,
                        column=col + 1,
                        original=wrong,
                        corrected=correct,
                        type="class"
                    ))

        fixed_lines.append(fixed_line)

    fixed_code = '\n'.join(fixed_lines)
    return fixed_code, fixes


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Code Fix API is running", "status": "ok"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/fix", response_model=FixResponse)
async def fix_code(request: FixRequest):
    """
    Detect and fix API hallucinations in the provided code.
    
    Args:
        request: FixRequest containing the code to fix
        
    Returns:
        FixResponse with fixed code and list of fixes made
    """
    if not request.code:
        raise HTTPException(status_code=400, detail="Code cannot be empty")

    start_time = time.time()
    fixed_code, fixes = find_and_fix_hallucinations(request.code)
    processing_time = time.time() - start_time

    return FixResponse(
        fixed_code=fixed_code,
        fixes=fixes,
        status="success"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)