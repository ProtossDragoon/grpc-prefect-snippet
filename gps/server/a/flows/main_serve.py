""" python3 -m gps.server.a.flows.main_serve
"""

# 내장
from pathlib import Path

# 서드파티
import dotenv

# 프로젝트
from gps.server.a.flows import main_flow

if __name__ == "__main__":
    dotenv.load_dotenv(Path("./.env"))  # NOTE: '.': project root
    main_flow.serve(name="PrefectServerA")
