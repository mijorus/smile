def tag_list_contains(tags: str, q: str) -> bool():
    tags_arr = tags.replace(', ', ',').split(',')
    for t in tags_arr:
        if t.lower().startswith(q.lower()):
            return True

    return False