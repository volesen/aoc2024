def is_variable(x):
    return x.startswith("?")


def extend_if_possible(variable, value, frame: dict) -> dict | None:
    if variable in frame:
        return match_part(frame[variable], value, frame)

    return {variable: value, **frame}


def match_part(pattern_part, fact_path, frame: dict) -> dict | None:
    if is_variable(pattern_part):
        return extend_if_possible(pattern_part, fact_path, frame)

    if pattern_part != fact_path:
        return None

    return frame


def match_pattern(pattern, fact, frame: dict) -> dict | None:
    for pattern_part, fact_part in zip(pattern, fact):
        frame = match_part(pattern_part, fact_part, frame)  # type: ignore
        if frame is None:
            return None

    return frame


def query_single(query, facts, frames):
    for frame in frames:
        for fact in facts:
            extended_frame = match_pattern(query, fact, frame)
            if extended_frame is not None:
                yield extended_frame


def query(queries, facts, frames):
    for query in queries:
        frames = query_single(query, facts, frames)

    return frames
