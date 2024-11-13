def actived_flags_count(flags: list[int]) -> int:
    count = 0
    for flag in flags:
        if flag == 0:
            count += 1
    return count
