import copy
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure repo/src is on path so `from src import app` works when running pytest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import app as app_module


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app_module.app)


# Preserve original activities and restore before/after each test to avoid state leakage
_ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = copy.deepcopy(_ORIGINAL_ACTIVITIES)
    yield
    app_module.activities = copy.deepcopy(_ORIGINAL_ACTIVITIES)
