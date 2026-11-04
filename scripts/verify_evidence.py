"""Audit recorded stage results against the fresh Maven/JaCoCo outputs."""
from pathlib import Path
import ast
import csv
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

def coverage(path):
    with path.open(encoding='utf-8', newline='') as stream:
        rows = [r for r in csv.DictReader(stream) if r['CLASS'] == 'ScholarshipCalculator']
    assert len(rows) == 1, path
    return rows[0]

def counts(row):
    return tuple(int(row[k]) for k in ('LINE_MISSED', 'LINE_COVERED', 'BRANCH_MISSED', 'BRANCH_COVERED'))

expected = {'A': (5, (9, 16, 19, 22)), 'B': (20, (0, 25, 0, 41)),
            'C': (22, (0, 25, 0, 41)), 'final': (29, (0, 25, 0, 41))}
for stage, (tests, values) in expected.items():
    log = (ROOT / f'results/mvn-verify-{stage}.txt').read_text(encoding='utf-8')
    assert 'BUILD SUCCESS' in log
    assert f'Tests run: {tests}, Failures: 0, Errors: 0, Skipped: 0' in log
    assert counts(coverage(ROOT / f'results/jacoco-{stage}.csv')) == values
    print(f'{stage}: {tests} tests; line/branch counters match recorded CSV')
fail = (ROOT / 'results/mvn-test-D-fail.txt').read_text(encoding='utf-8')
assert 'Tests run: 29, Failures: 1, Errors: 0, Skipped: 0' in fail
assert 'letterGrade_sixty_returnsD' in fail and 'expected: <D> but was: <F>' in fail
assert 'BUILD FAILURE' in fail
print('D: exact 60 boundary failure recorded')
gate = (ROOT / 'results/mvn-verify-gate-fail.txt').read_text(encoding='utf-8')
assert 'Tests run: 5, Failures: 0, Errors: 0, Skipped: 0' in gate
assert 'branches covered ratio is 0.53, but expected minimum is 0.90' in gate
assert 'BUILD FAILURE' in gate
print('Gate: passing happy path tests correctly rejected for insufficient coverage')
fresh = coverage(ROOT / 'target/site/jacoco/jacoco.csv')
assert counts(fresh) == expected['final'][1]
recorded = coverage(ROOT / 'results/jacoco-final.csv')
assert fresh == recorded, 'Fresh coverage differs from committed final CSV'
reports = list((ROOT / 'target/surefire-reports').glob('TEST-*.xml'))
assert reports
summaries = [ET.parse(p).getroot().attrib for p in reports]
assert sum(int(r['tests']) for r in summaries) == 29
assert all(int(r[k]) == 0 for r in summaries for k in ('failures', 'errors', 'skipped'))
source = (ROOT / 'src/test/java/mn/edu/must/sqat/ScholarshipCalculatorTest.java').read_text()
names = set(re.findall(r'void\s+(\w+)\s*\(', source))
diagram = (ROOT / 'scripts/draw_cfg.py').read_text()
for assignment in ast.parse(diagram).body:
    if isinstance(assignment, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id in ('true_names', 'false_names')
        for t in assignment.targets
    ):
        for suffix in ast.literal_eval(assignment.value).values():
            assert 'scholarship_' + suffix in names, suffix
assert (ROOT / 'cfg.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
print('Fresh build: 29 passing tests; 25/25 lines and 41/41 branches; CFG method names match')
