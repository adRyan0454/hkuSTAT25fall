import csv
import re
import html
from pathlib import Path


def _normalize_studio_key(name: str) -> str:
    """
    将 studio 名称规范化为“比较用 key”，用于判断是否为同一家公司。

    规则大致为：
    - HTML 反转义（A&amp;E -> A&E）
    - 全部转小写
    - 去掉标点（. , / & 等会被视为分隔符）
    - 去掉常见后缀词：pictures, films, entertainment, home video, distribution 等
    - 去掉 the, company, studios 等泛泛词

    返回的 key 仅用于“是否同一家”的判断，不会直接写回 CSV。
    """
    if not isinstance(name, str):
        name = "" if name is None else str(name)

    # HTML 实体反转义
    s = html.unescape(name)
    s = s.lower().strip()
    if not s:
        return ""

    # 一些常见“大厂”的写法标准化，便于不同变体归并到同一个 key
    # 这里只改“比较用的 s”，不改真正写回 CSV 的名称。
    # 20th / twentieth century fox
    s = s.replace("twentieth century fox", "20th century fox")
    s = s.replace("twentieth century", "20th century")
    # dreamworks 相关
    s = s.replace("dream works", "dreamworks")
    # lionsgate 相关
    s = s.replace("lions gate", "lionsgate")
    # new line cinema 相关
    s = s.replace("new line cinema", "newline cinema")
    s = s.replace("new line", "newline")
    # miramax
    s = s.replace("miramax films", "miramax")
    # weinstein
    s = s.replace("the weinstein company", "weinstein company")
    s = s.replace("the weinstein co.", "weinstein company")
    s = s.replace("the weinstein co", "weinstein company")
    # warner bros / brothers / wb
    s = s.replace("warner brothers", "warner bros")
    s = s.replace("warners", "warner bros")

    # 将标点统一替换成空格，只保留字母数字和空白
    s = re.sub(r"[^\w\s]", " ", s)

    # 拆成单词，并去掉常见“噪音词”和公司后缀
    stop_words = {
        # 冠词/泛词
        "the",
        "company",
        "co",
        "co.",
        "corp",
        "corp.",
        "corporation",
        "group",
        "inc",
        "inc.",
        "ltd",
        "ltd.",
        "llc",
        "usa",
        "us",
        # 影视行业常见后缀
        "pictures",
        "picture",
        "films",
        "film",
        "studios",
        "studio",
        "entertainment",
        "home",
        "video",
        "videos",
        "distribution",
        "distributing",
        "releasing",
        "international",
        "inter",
        "television",
    }

    parts = [p for p in s.split() if p and p not in stop_words]
    if not parts:
        return ""

    # 以空格拼回，作为统一 key
    return " ".join(parts)


def clean_movies(
    src_path: Path = Path(r"E:\AAStat\8000 Project\Acode\sql\data\movies.csv"),
    out_path: Path = Path(r"E:\AAStat\8000 Project\Acode\sql\data\movies_clean.csv"),
) -> None:
    """
    从 movies.csv 生成 movies_clean.csv。

    当前数据中 movies.csv 与 movies_clean.csv 的字段完全一致，
    因此这里主要做的是：
    - 读取原始 movies.csv
    - 对所有字符串字段做 strip() 去掉首尾空白
    - 原样写出为 movies_clean.csv（保留列顺序）
    """

    if not src_path.exists():
        raise FileNotFoundError(f"源文件不存在: {src_path}")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    with src_path.open(encoding="utf-8", newline="") as f_in, out_path.open(
        "w", encoding="utf-8", newline=""
    ) as f_out:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames
        if fieldnames is None:
            raise ValueError("源文件没有表头（header），无法清洗。")

        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        # 记录“标准 Studio 名称”：key 为规范化后的 studio key，value 为第一次出现的原始名称
        studio_canonical: dict[str, str] = {}

        for row in reader:
            cleaned = {}
            for k, v in row.items():
                # 统一把 None 写回空字符串，其它字符串去掉首尾空白
                if v is None:
                    cleaned[k] = ""
                elif isinstance(v, str):
                    cleaned[k] = v.strip()
                else:
                    cleaned[k] = v

            # === Studio 名称标准化 ===
            # 思路：对 studio 做一个“key 化”，如果 key 一致，则认为是同一家，
            # 用第一次出现的原始写法作为后续行的统一名称。
            studio_raw = cleaned.get("studio", "")
            if isinstance(studio_raw, str):
                key = _normalize_studio_key(studio_raw)
                if key:
                    if key not in studio_canonical:
                        # 首次遇到该 key：把当前原始名称作为标准名称记下来
                        studio_canonical[key] = studio_raw
                    else:
                        # 后续再遇到同一个 key：统一替换为第一次的写法
                        cleaned["studio"] = studio_canonical[key]

            # 规则调整：
            # 1. title 为空（或全是空白） => 丢弃整行
            # 2. 任意字段在清洗后为空字符串 => 认为该行存在缺失，也丢弃整行

            # 1) 检查 title
            title_val = cleaned.get("title", "")
            if not isinstance(title_val, str):
                title_val = str(title_val) if title_val is not None else ""
            if title_val.strip() == "":
                continue

            # 2) 检查是否存在任意字段缺失（空字符串）
            has_missing = False
            for v in cleaned.values():
                # 数值字段不会是 ""，这里只针对字符串缺失
                if isinstance(v, str) and v == "":
                    has_missing = True
                    break

            if has_missing:
                # 这条记录在 check 中会被视为“有缺失”，因此在 clean 阶段直接删除
                continue

            writer.writerow(cleaned)


if __name__ == "__main__":
    clean_movies()

