def annotations(arg1, arg2: str):
    return " ".join(["annotations:", arg1, arg2])


def annotations_with_defaults(arg1, arg2: "has a default" = "default"):  # noqa: F722
    return " ".join(["annotations:", arg1, arg2])
