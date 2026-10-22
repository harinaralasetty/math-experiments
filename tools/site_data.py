"""Shared source model and display formatting; no manually entered result totals."""
import json
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFICATION_FILES = ('verification.json', 'stage3-verification.json', 'stage4-verification.json')

def load_verification(root=ROOT):
    runs = [json.loads((root/'oeis/data'/name).read_text())
            for name in VERIFICATION_FILES]
    return {key: [row for run in runs for row in run[key]] for key in ['sequences', 'methods']}

def duration(seconds):
    value = float(seconds)
    unit = 's'
    if value >= 60:
        value /= 60
        unit = 'min'
    # Keep two significant digits, including a trailing zero where necessary.
    rounded = format(Decimal(f'{value:.2g}'), 'f')
    return f'{rounded} {unit}'
