""" python3 -m gps.server.a.flows.main_serve
"""

# 내장
import os
from pathlib import Path

# 서드파티
import dotenv

# 프로젝트
from gps.server.a.flows import server_a_flow

if __name__ == "__main__":
    envfile_path = Path("./envs/network.env")
    assert os.path.exists(envfile_path)
    dotenv.load_dotenv(envfile_path)  # NOTE: '.': project root
    server_a_flow.serve(name="PrefectServerA")
