import csv, pathlib, re

src = pathlib.Path(r"E:\AAStat\8000 Project\Acode\sql\data\movies_clean.csv")
out = pathlib.Path(r"E:\AAStat\8000 Project\Acode\sql\data\raw_people_links.csv")


def _clean_credit_field(raw: str) -> str:
    """
    清洗导演/编剧/演员整字段：
    - 删除括号及其中内容（包括其中的逗号）
    - 额外处理“未闭合括号”的脏数据：从最后一个 '(' 一直到末尾都去掉
    """
    s = (raw or "").strip()
    if not s:
        return ""
    # 正常的 (...) 块
    s = re.sub(r"\s*\([^)]*\)", "", s)
    # 如果还有剩余的“未闭合括号”，比如 "xxx (short story \"Button"
    if "(" in s and ")" not in s:
        s = re.sub(r"\s*\([^)]*$", "", s)
    return s.strip()


with src.open(encoding="utf-8", newline="") as f, out.open("w", encoding="utf-8", newline="") as g:
    r = csv.DictReader(f)
    w = csv.writer(g)
    w.writerow(["title", "year", "role_type", "person_name"])
    for row in r:
        title, year = row["title"], row["year"]

        # 先在“整字段”层面去掉所有括号中的补充说明（包括其中的逗号），
        # 再用逗号拆分名字，避免像 "Button, Button" 这类内容被拆成独立的人名。
        director_field = _clean_credit_field(row.get("director", ""))
        writer_field = _clean_credit_field(row.get("writer", ""))
        actors_field = _clean_credit_field(row.get("actors", ""))

        def emit(role_type: str, field: str) -> None:
            for name in field.split(","):
                name = name.strip()
                # 去掉字段中多余的引号（如 Frank Darabont""" 这种情况）
                name = name.strip('"').strip()
                # 特殊脏数据过滤：像 The Box 里残留的 "Button" / "Button"""")" 这种非人名
                lowered = name.lower()
                if (
                    not name
                    or lowered == "button"
                    or (lowered.startswith("button") and " " not in lowered)
                ):
                    continue
                w.writerow([title, year, role_type, name])

        emit("Director", director_field)
        emit("Writer", writer_field)
        emit("Actor", actors_field)