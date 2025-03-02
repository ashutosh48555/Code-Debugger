from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_integration import get_ai_suggestions, apply_quick_fix
from subprocess import run, PIPE

app = FastAPI()

# Root route for testing
@app.get("/")
async def root():
    return {"message": "Welcome to the AI-Powered Code Debugger!"}

class CodeRequest(BaseModel):
    code: str

@app.post("/run")
async def run_code(request: CodeRequest):
    code = request.code
    errors, output = [], ""

    # Check for syntax errors
    try:
        compile(code, "<string>", "exec")
    except SyntaxError as e:
        errors.append(str(e))

    # Execute code in a sandboxed environment
    if not errors:
        try:
            result = run(["python", "-c", code], stdout=PIPE, stderr=PIPE, text=True, timeout=5)
            if result.stderr:
                errors.append(result.stderr.strip())
            else:
                output = result.stdout.strip()
        except Exception as e:
            errors.append(f"Execution failed: {str(e)}")

    # Get AI suggestions
    suggestions = get_ai_suggestions(code, errors)

    return {"errors": errors, "output": output, "suggestions": suggestions}

@app.post("/quickfix")
async def quick_fix_code(request: CodeRequest):
    code = request.code
    fixed_code = apply_quick_fix(code)  # Use AI to fix the code
    return {"fixed_code": fixed_code}