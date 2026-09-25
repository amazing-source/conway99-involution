# Linux Python for generating CNFs with LF line endings (LAB_INSTRUCTIONS.md §0b, §3), same pins as the audit.
# docker build -t c99py -f code/z2/Dockerfile.py code/z2
# docker run --rm -v "<repo>:/repo" -w /work c99py python /repo/code/z2/orbit_sat.py --m 7 --case sib --out k14_sib.cnf
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir "python-sat==1.9.dev15" "numpy==2.5.3" "sympy==1.14.0" "ortools==9.15.6755"
