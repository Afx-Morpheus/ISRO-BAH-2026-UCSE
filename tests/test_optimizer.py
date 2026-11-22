import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.optimizer import optimize
import json
ZONES=json.loads((Path(__file__).resolve().parents[1]/'data'/'zones.json').read_text())

def test_budget_not_exceeded():
    result=optimize(ZONES,150,'balanced')
    assert result['allocated_crore'] <= 150
    assert result['allocated_crore'] >= 0

def test_modes_are_supported():
    for mode in ('budget','balanced','cooling'):
        assert optimize(ZONES,100,mode)['mode']==mode

def test_invalid_mode_rejected():
    try: optimize(ZONES,100,'magic')
    except ValueError: return
    assert False, 'invalid mode should raise ValueError'
