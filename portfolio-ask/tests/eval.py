import yaml
from portfolio_ask.main import run


def check_case(result, expected):
    structured = result.get("structured", {})

    for key, expected_value in expected.items():
        actual_value = structured.get(key)

        # handle booleans (like flags)
        if isinstance(expected_value, bool):
            if expected_value is True and not actual_value:
                return False, f"{key} missing or false"
        else:
            if actual_value != expected_value:
                return False, f"{key} mismatch: expected {expected_value}, got {actual_value}"

    return True, "OK"


def run_eval():
    with open("evals/cases.yaml", "r") as f:
        cases = yaml.safe_load(f)

    passed = 0
    total = len(cases)

    print("\n========== EVALUATION ==========\n")

    for i, case in enumerate(cases, 1):
        question = case["question"]
        expected = case["expected"]

        result = run(question)

        ok, msg = check_case(result, expected)

        status = "PASS" if ok else "FAIL"

        print(f"{i}. {status}")
        print("Q:", question)
        print("Expected:", expected)
        print("Got:", result["structured"])
        print("Validation:", result["validation"])
        print("Reason:", msg)
        print("-" * 40)

        if ok:
            passed += 1

    print(f"\nRESULT: {passed}/{total} passed")


if __name__ == "__main__":
    run_eval()