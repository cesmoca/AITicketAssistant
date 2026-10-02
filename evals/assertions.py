from evals.loader import absent_selector


def find_matches(tickets: list[dict], selector: dict) -> list[dict]:
    return [ticket for ticket in tickets if all(ticket.get(field) == value for field, value in selector.items())]


def compare_fields(expected: dict, actual: dict, label: str) -> list[str]:
    errors = []
    for field, value in expected.items():
        if field not in actual:
            errors.append(f"{label}.{field}: missing; expected {value!r}")
        elif actual[field] != value:
            errors.append(f"{label}.{field}: expected {value!r}; actual {actual[field]!r}")
    return errors


def compare_case(expected: dict, actual: dict) -> list[str]:
    errors = compare_fields(expected["response"], actual["response"], "response")
    tickets = actual["database"]["tickets"]
    database = expected["database"]
    errors.extend(compare_fields(
        {"ticket_count": database["ticket_count"]}, actual["database"], "database",
    ))
    for ticket in database["tickets"]:
        selector = ticket["match"]
        matches = find_matches(tickets, selector)
        label = f"ticket match={selector!r}"
        if len(matches) != 1:
            errors.append(f"{label}: expected exactly 1 match; actual {len(matches)}")
        else:
            errors.extend(compare_fields(ticket["assert"], matches[0], label))
    for entry in database.get("absent", []):
        selector = absent_selector(entry)
        matches = find_matches(tickets, selector)
        if matches:
            errors.append(f"absent match={selector!r}: expected 0 matches; actual {len(matches)}")
    return errors
