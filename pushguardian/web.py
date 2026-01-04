"""FastAPI web demo for diff analysis."""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .graph import run_guardian

app = FastAPI(title="PushGuardian Web Demo", version="0.1.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for web mode
REPORTS_CACHE = {}
CACHE_DIR = Path(".pushguardian_cache")
CACHE_DIR.mkdir(exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Simple HTML form for diff input."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>PushGuardian Web Demo</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; }
            h1 { color: #2c3e50; }
            textarea { width: 100%; height: 300px; font-family: monospace; }
            button { background: #3498db; color: white; padding: 10px 20px; border: none; cursor: pointer; font-size: 16px; }
            button:hover { background: #2980b9; }
            .result { margin-top: 30px; padding: 20px; background: #ecf0f1; border-radius: 5px; }
            pre { background: #2c3e50; color: #ecf0f1; padding: 15px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>🛡️ PushGuardian Web Demo</h1>
        <p>Paste your git diff below or upload a diff file to analyze security and best-practice issues.</p>

        <form id="analyzeForm">
            <h3>Option 1: Paste Diff Text</h3>
            <textarea name="diff_text" id="diff_text" placeholder="Paste git diff output here..."></textarea>

            <h3>Option 2: Upload Diff File</h3>
            <input type="file" name="diff_file" id="diff_file" accept=".txt,.diff,.patch">

            <br><br>
            <button type="submit">🔍 Analyze Diff</button>
        </form>

        <div id="result" class="result" style="display:none;">
            <h2>Analysis Result</h2>
            <div id="resultContent"></div>
        </div>

        <script>
            document.getElementById('analyzeForm').addEventListener('submit', async (e) => {
                e.preventDefault();

                const formData = new FormData();
                const diffText = document.getElementById('diff_text').value;
                const diffFile = document.getElementById('diff_file').files[0];

                if (diffFile) {
                    formData.append('diff_file', diffFile);
                } else if (diffText) {
                    formData.append('diff_text', diffText);
                } else {
                    alert('Please provide either diff text or upload a file.');
                    return;
                }

                const resultDiv = document.getElementById('result');
                const resultContent = document.getElementById('resultContent');

                resultDiv.style.display = 'block';
                resultContent.innerHTML = '<p>⏳ Analyzing...</p>';

                try {
                    const response = await fetch('/analyze-diff', {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();

                    if (response.ok) {
                        let html = `
                            <p><strong>Decision:</strong> <span style="color: ${data.decision === 'block' ? 'red' : 'green'}">${data.decision.toUpperCase()}</span></p>
                            <p><strong>Severity:</strong> ${data.severity.toUpperCase()}</p>
                            <p><strong>Risk Score:</strong> ${data.risk_score.toFixed(2)}/1.00</p>
                            <p><strong>Findings:</strong> ${data.findings_count}</p>
                        `;

                        if (data.report_id) {
                            html += `<p><a href="/download/${data.report_id}" download>📥 Download Full Report (MD)</a></p>`;
                        }

                        html += `<h3>Full Report (Preview)</h3><pre>${escapeHtml(data.report_md)}</pre>`;

                        resultContent.innerHTML = html;
                    } else {
                        resultContent.innerHTML = `<p style="color:red;">Error: ${data.detail || 'Analysis failed'}</p>`;
                    }
                } catch (err) {
                    resultContent.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
                }
            });

            function escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }
        </script>
    </body>
    </html>
    """


@app.post("/analyze-diff")
async def analyze_diff(
    diff_text: Optional[str] = Form(None), diff_file: Optional[UploadFile] = File(None)
):
    """
    Analyze git diff for security and best-practice issues.

    Args:
        diff_text: Raw diff text (form field)
        diff_file: Diff file upload

    Returns:
        JSON response with analysis results
    """
    # Get diff content
    if diff_file:
        content = await diff_file.read()
        diff_content = content.decode("utf-8")
    elif diff_text:
        diff_content = diff_text
    else:
        raise HTTPException(status_code=400, detail="No diff provided")

    if not diff_content.strip():
        raise HTTPException(status_code=400, detail="Empty diff")

    try:
        # Run guardian in web mode
        state = run_guardian(diff_content, mode="web")

        # Generate report ID
        report_id = str(uuid.uuid4())

        # Save report to cache
        report_path = CACHE_DIR / f"{report_id}.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(state["report_md"])

        REPORTS_CACHE[report_id] = {
            "report_md": state["report_md"],
            "report_path": str(report_path),
            "timestamp": datetime.now().isoformat(),
        }

        # Return summary
        return JSONResponse(
            content={
                "report_id": report_id,
                "decision": state["decision"],
                "severity": state["severity"],
                "risk_score": state["risk_score"],
                "findings_count": len(state["hard_findings"]) + len(state["soft_findings"]),
                "report_md": state["report_md"],
                "errors": state.get("errors", []),
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/download/{report_id}")
async def download_report(report_id: str):
    """
    Download markdown report.

    Args:
        report_id: Report UUID

    Returns:
        File download response
    """
    if report_id not in REPORTS_CACHE:
        raise HTTPException(status_code=404, detail="Report not found")

    report_path = REPORTS_CACHE[report_id]["report_path"]

    if not Path(report_path).exists():
        raise HTTPException(status_code=404, detail="Report file not found")

    return FileResponse(
        report_path,
        media_type="text/markdown",
        filename=f"pushguardian_report_{report_id[:8]}.md",
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "PushGuardian Web Demo"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
