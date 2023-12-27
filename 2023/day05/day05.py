def range_intersect(r1, r2):
    return range(max(r1.start, r2.start), min(r1.stop, r2.stop))


def range_minus(r1, r2):
    rr1 = min(r1.start, r2.stop), min(r1.stop, r2.start)
    rr2 = r2.stop, r1.stop
    return [range(r[0], r[1]) for r in [rr1, rr2] if r[0] < r[1]]


def map_range(mapper, src, dest, src_ranges: list):
    map_ranges = mapper[src][dest]
    mapped = list()  # a list of ranges
    while len(src_ranges) > 0:
        s = src_ranges.pop()
        for m_range in map_ranges:
            sect = range_intersect(s, m_range["src_range"])
            if len(sect) == 0:
                continue

            # Transform the intersection to the new range
            off = m_range["src_range"].start - m_range["dest_range"].start
            mapped.append(range(sect.start - off, sect.stop - off))

            # Now remove the intersection from the original range (since we processed it already)
            # But we have to process those parts which were not part of the intersection
            src_ranges += range_minus(s, sect)
            break
        else:  # s did not match to any range
            mapped.append(s)
    return mapped


def transform_range(mapper, range_list, source="seed"):
    while source in mapper:
        destination = next(iter(mapper[source]))  # should be exactly 1
        range_list = map_range(mapper, source, destination, range_list)
        source = destination

    return [l.start for l in range_list]  # start is the smallest location


def day05():
    file1 = open("2023/day05/input_1.txt", "r")
    lines = file1.readlines()
    lines = [l.strip() for l in lines]

    seeds = [int(i) for i in lines[0].split(":")[1].strip().split(" ")]

    mapper = dict()
    for l in lines[1:]:
        if l == "":
            continue
        elif "map" in l:
            (
                map_from,
                _,
                map_to,
            ) = l[
                :-5
            ].split("-")
            mapper[map_from] = dict()
            mapper[map_from][map_to] = list()
        else:
            dest, src, ranger = (int(i) for i in l.strip().split(" "))
            obj = {
                "dest_range": range(dest, dest + ranger),
                "src_range": range(src, src + ranger),
                "range": ranger,
            }
            mapper[map_from][map_to].append(obj)

    # Part 1
    seeds_1 = [range(s, s + 1) for s in seeds]
    min_loc_numbers = transform_range(mapper, seeds_1)
    print(f"Solution Day 5.1: {min(min_loc_numbers)}")

    # Part 2
    seeds_2 = [
        range(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)
    ]
    min_loc_numbers = transform_range(mapper, seeds_2)
    print(f"Solution Day 5.2: {min(min_loc_numbers)}")


if __name__ == "__main__":
    assert range_minus(range(4, 9), range(1, 9)) == []
    assert range_minus(range(1, 9), range(1, 9)) == []
    assert range_minus(range(1, 9), range(3, 7)) == [range(1, 3), range(7, 9)]
    assert range_minus(range(3, 8), range(1, 6)) == [range(6, 8)]
    assert range_minus(range(1, 6), range(3, 8)) == [range(1, 3)]
    assert range_minus(range(1, 6), range(1, 5)) == [range(5, 6)]
    assert range_minus(range(1, 6), range(2, 6)) == [range(1, 2)]
    assert range_minus(range(2, 6), range(1, 7)) == []
    day05()
