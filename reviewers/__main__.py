import sh


def get_files_for_blame(diff: str) -> dict:
    diff_lines = diff.splitlines()
    skipping = 1
    searching_filename = 2
    searching_chunk = 3
    state = skipping
    chunks = {}
    current_chunk_filename = None

    for line in diff_lines:
        if state == skipping:
            if line[:4] != 'diff':
                continue

            state = searching_filename
        elif state == searching_filename:
            if line[:3] != '---':
                continue

            if line[4:] == '/dev/null':
                continue

            current_chunk_filename = line[6:]
            state = searching_chunk
        elif state == searching_chunk:
            if line[:2] != '@@':
                continue

            if current_chunk_filename not in chunks:
                chunks[current_chunk_filename] = []

            line_numbers = line.split(" ")[1]
            (start_line, offset) = map(int, line_numbers[1:].split(","))
            chunks[current_chunk_filename].append((start_line, offset))

            state = skipping

    return chunks


def get_authors_from_blame(blame: str) -> dict:
    authors = {}
    author_name = "unknown"
    for line in blame.splitlines():
        if line[0] == "\t":
            continue

        key, value = line.split(" ", 1)

        if key == "author":
            author_name = value
            continue

        if key != "author-mail":
            continue

        author_email = value[1:].split(">", 1)[0]
        if author_email not in authors:
            authors[author_email] = {
                "count": 0,
                "name": author_name,
            }

        authors[author_email]["count"] += 1

    return authors


def add_authors_to_reviewers(reviewers: dict, authors: dict) -> dict:
    for author_email, author_info in authors.items():
        if author_email not in reviewers:
            reviewers[author_email] = {
                "name": author_info['name'],
                "chunks_count": 0,
                "total_count": 0,
            }
        reviewers[author_email]["chunks_count"] += 1
        reviewers[author_email]["total_count"] += author_info["count"]
    return reviewers


def main():
    git = sh.git.bake("--no-pager")
    merge_base = git("merge-base", "master", "HEAD")
    merge_base_rev = str(merge_base).strip()
    branch_diff_res = git.diff(merge_base_rev + "..", "--no-color")
    branch_diff = str(branch_diff_res).strip()

    files_for_blame = get_files_for_blame(branch_diff)
    reviewers = {}
    for filename, lines_info in files_for_blame.items():
        for line, offset in lines_info:
            print("Blaming %s %s,+%d..." % (filename, line, offset))
            blame = git.blame("-L", "%d,+%d" % (line, offset), "--line-porcelain", merge_base_rev, "--", filename)
            authors = get_authors_from_blame(blame)
            reviewers = add_authors_to_reviewers(reviewers, authors)

    print()
    reviewers_table = sorted(reviewers.items(), reverse=True, key=lambda x: (x[1]["chunks_count"], x[1]["total_count"]))
    for email, reviewer_info in reviewers_table:
        print("{name:>25} {:>40} {chunks_count:>5}.{total_count}".format(email, **reviewer_info))


if __name__ == "__main__":
    main()
