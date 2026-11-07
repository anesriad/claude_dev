from claude_assist.agent import run_agent
from evals.eval_set import EVALS


# Check one evaluation result against its success criteria.
def check_case(case, result):
    answer = result["answer"].lower()
    tools_used = result["tools_used"]
    steps = result["steps"]

    content_ok = all(
        item.lower() in answer
        for item in case["must_contain"]
    )

    tool_ok = (
        case["expected_tool"] is None
        or case["expected_tool"] in tools_used
    )

    steps_ok = steps <= case["max_steps"]
    
    #Only pass the case when all three checks are good.
    return content_ok and tool_ok and steps_ok


# Run every evaluation case and print a short report.
# Think of it as the test runner.
def main():
    passed = 0

    for case in EVALS:
        print(f"\n--- {case['name']} ---")

        result = run_agent(
            case["input"],
            return_trace=True
        )

        ok = check_case(case, result)

        print("answer:", result["answer"])
        print("tools:", result["tools_used"])
        print("steps:", result["steps"])
        print("status:", "PASS" if ok else "NEEDS REVIEW")

        if ok:
            passed += 1

    print(f"\n{passed}/{len(EVALS)} passed")


if __name__ == "__main__":
    main()
