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
        <title>PushGuardian 웹 데모</title>
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
        <h1>🛡️ PushGuardian 웹 데모</h1>
        <p>아래에 git diff를 붙여 넣거나 diff 파일을 업로드하여 보안 이슈와 모범 사례 위반을 분석해 보세요.</p>

        <form id="analyzeForm">
            <h3>옵션 1: Diff 텍스트 직접 붙여넣기</h3>
            <textarea name="diff_text" id="diff_text" placeholder="여기에 git diff 출력 결과를 붙여 넣으세요..."></textarea>

            <h3>옵션 2: Diff 파일 업로드</h3>
            <input type="file" name="diff_file" id="diff_file" accept=".txt,.diff,.patch">

            <br><br>
            <button type="submit">🔍 Diff 분석하기</button>
        </form>

        <div id="result" class="result" style="display:none;">
            <h2>분석 결과</h2>
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
                    alert('Diff 텍스트를 입력하거나 파일을 업로드해 주세요.');
                    return;
                }

                const resultDiv = document.getElementById('result');
                const resultContent = document.getElementById('resultContent');

                resultDiv.style.display = 'block';
                resultContent.innerHTML = '<p>⏳ 분석 중입니다...</p>';

                try {
                    const response = await fetch('/analyze-diff', {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();

                    if (response.ok) {
                        // 한글 변환 맵핑
                        const decisionMap = {
                            'allow': '허용',
                            'block': '차단',
                            'override': '오버라이드'
                        };
                        const severityMap = {
                            'low': '낮음',
                            'medium': '중간',
                            'high': '높음',
                            'critical': '심각'
                        };

                        const decisionKo = decisionMap[data.decision.toLowerCase()] || data.decision.toUpperCase();
                        const severityKo = severityMap[data.severity.toLowerCase()] || data.severity.toUpperCase();

                        let html = `
                            <p><strong>결정:</strong> <span style="color: ${data.decision === 'block' ? 'red' : 'green'}">${decisionKo}</span></p>
                            <p><strong>심각도:</strong> ${severityKo}</p>
                            <p><strong>위험 점수:</strong> ${data.risk_score.toFixed(2)}/1.00</p>
                            <p><strong>발견된 이슈 수:</strong> ${data.findings_count}</p>
                        `;

                        if (data.report_id) {
                            html += `<p><a href="/download/${data.report_id}" download>📥 전체 리포트 다운로드 (MD)</a></p>`;
                        }

                        html += `<h3>전체 리포트 (미리보기)</h3><pre>${escapeHtml(data.report_md)}</pre>`;

                        resultContent.innerHTML = html;
                    } else {
                        resultContent.innerHTML = `<p style="color:red;">오류: ${data.detail || '분석에 실패했습니다'}</p>`;
                    }
                } catch (err) {
                    resultContent.innerHTML = `<p style="color:red;">오류: ${err.message}</p>`;
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
        raise HTTPException(status_code=400, detail="Diff 내용이 제공되지 않았습니다.")

    if not diff_content.strip():
        raise HTTPException(status_code=400, detail="Diff 내용이 비어 있습니다.")

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
        raise HTTPException(status_code=500, detail=f"분석에 실패했습니다: {str(e)}")


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
        raise HTTPException(status_code=404, detail="리포트를 찾을 수 없습니다.")

    report_path = REPORTS_CACHE[report_id]["report_path"]

    if not Path(report_path).exists():
        raise HTTPException(status_code=404, detail="리포트 파일을 찾을 수 없습니다.")

    return FileResponse(
        report_path,
        media_type="text/markdown",
        filename=f"pushguardian_report_{report_id[:8]}.md",
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "PushGuardian 웹 데모"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
