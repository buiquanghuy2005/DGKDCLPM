"""Validate saved evidence; the project report is BAO_CAO.pdf at the repo root."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

TOOL = Path(__file__).resolve().parents[1]
EVIDENCE = TOOL / "experiments" / "2026-10-19"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(name):
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8-sig"))


def cases(name):
    result = []
    for case in ET.parse(EVIDENCE / name).getroot().iter("testcase"):
        status = "failed" if case.find("failure") is not None else (
            "error" if case.find("error") is not None else (
                "skipped" if case.find("skipped") is not None else "passed"))
        result.append((case.get("classname", ""), case.get("name", ""), status))
    require(len(result) == len({(c[0], c[1]) for c in result}), f"Duplicate cases: {name}")
    return result


def summary(rows):
    counts = Counter(row[2] for row in rows)
    return {"total": len(rows), "passed": counts["passed"], "failed": counts["failed"],
            "error": counts["error"], "skipped": counts["skipped"]}


def check():
    full = cases("selenium-all-122951/report.xml")
    expected = {"total": 85, "passed": 75, "failed": 10, "error": 0, "skipped": 0}
    require(summary(full) == expected, "Full Selenium results differ from saved baseline")
    stored = read_json("selenium-all-122951/run.json")
    require([(c["classname"], c["name"], c["status"]) for c in stored["report"]["cases"]] == full,
            "XML and stored cases differ")
    require(stored["report"]["summary"] == expected, "Stored run summary mismatch")
    for name in ["selenium-all-122951/summary.json", "selenium-full-results.json"]:
        require(read_json(name)["summary"] == expected, f"Summary mismatch: {name}")

    vitest = cases("vitest-ui.xml")
    require(summary(vitest) == {"total": 22, "passed": 22, "failed": 0, "error": 0, "skipped": 0},
            "Vitest summary mismatch")
    require(vitest == cases("vitest-cli.xml"), "CLI/UI Vitest cases differ")
    small = cases("selenium-notebook-122623/report.xml")
    require(summary(small) == {"total": 10, "passed": 10, "failed": 0, "error": 0, "skipped": 0},
            "Small Selenium group summary mismatch")
    require(small == cases("selenium-notebook-cli-2026-10-19T12-58-44-003Z/report.xml"),
            "CLI/UI Selenium cases differ")

    imports = read_json("xml-compatibility.json")
    require(imports["files"] == 70 and imports["totalTestcaseRecords"] == 115 and imports["allMatch"],
            "Historical XML evidence changed")

    log = (EVIDENCE / "tool-tests-after-selenium.log").read_text(encoding="utf-8-sig")
    tool_count = 0
    for module, count in [("gemini", 4), ("hsk-test-environment", 3), ("junit", 7), ("runner", 6), ("server", 1)]:
        source = (TOOL / "tests" / f"{module}.test.ts").read_text(encoding="utf-8-sig")
        names = re.findall(r"^test\('([^']+)'", source, re.M)
        require(len(names) == count, f"Tool tests changed: {module}")
        for name in names:
            require(any(line.startswith("✔ " + name + " (") for line in log.splitlines()),
                    f"No passing log entry: {name}")
        tool_count += count
    require(tool_count == 21 and re.search(r"tests 21\b", log)
            and re.search(r"pass 21\b", log) and re.search(r"fail 0\b", log), "Tool totals differ")

    judgements = read_json("ai-judgements.json")
    require(len(judgements["results"]) == 10 and Counter(c["classification"] for c in judgements["results"])
            == Counter({"đúng": 7, "đúng một phần": 3}), "Preliminary AI results changed")
    for item in judgements["results"]:
        cause, action = item["causeScore"], item["actionScore"]
        require(cause in (0, 1, 2) and action in (0, 1, 2), "Invalid AI rubric scores")
        classification = "đúng" if cause == action == 2 else (
            "đúng một phần" if cause + action >= 2 else "sai")
        require(item["classification"] == classification, f"AI classification mismatch: {item['id']}")
    totals = judgements["summary"]
    require(totals["total"] == 10 and totals["correct"] == 7 and totals["partlyCorrect"] == 3
            and totals["incorrect"] == 0, "AI summary mismatch")

    defects = Counter()
    for _, name, status in full:
        if status != "failed":
            continue
        if name == "test_register_whitespace_name": defect = "HSK-001"
        elif name.startswith("test_select_level_and_return["): defect = "HSK-002"
        elif name == "test_stats_calendar_and_ranges": defect = "HSK-003"
        elif name == "test_notebook[NOTE-04]": defect = "HSK-004"
        else: raise ValueError(f"Unmapped failure: {name}")
        defects[defect] += 1
    require(defects == Counter({"HSK-001": 1, "HSK-002": 7, "HSK-003": 1, "HSK-004": 1}),
            "Defect counts differ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Compatibility flag; validation is always read-only")
    parser.parse_args()
    check()
    print("OK: saved evidence matches (21 tool tests, 22 Vitest, 85 Selenium: 75 PASS/10 FAIL); no files generated.")
