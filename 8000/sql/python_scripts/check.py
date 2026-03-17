import csv
from pathlib import Path


def check_csv(
    src_path: Path = Path(r"E:\AAStat\8000 Project\Acode\sql\data\movies_clean.csv"),
) -> None:
    """
    检查给定 CSV 文件的字段缺失情况。

    功能：
    1. 检查 title 是否有缺失（为空或全是空白）。
    2. 对每一列统计“该列值为空（或全是空白）”的行数。
    """

    if not src_path.exists():
        raise FileNotFoundError(f"源文件不存在: {src_path}")

    with src_path.open(encoding="utf-8", newline="") as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames
        if fieldnames is None:
            raise ValueError("源文件没有表头（header），无法检查。")

        # 初始化统计
        total_rows = 0
        title_missing = 0
        # 每列缺失计数
        missing_per_field = {name: 0 for name in fieldnames}
        # 记录部分字段缺失的具体行，方便排查（目前关注 actors / language / studio）
        detail_fields = {"actors", "language", "studio"}
        missing_detail = {name: [] for name in detail_fields}

        for row in reader:
            total_rows += 1

            # 标准化并检查每一列
            for col in fieldnames:
                val = row.get(col, "")
                if val is None:
                    val_stripped = ""
                else:
                    val_stripped = str(val).strip()

                # 字段缺失统计：值为空字符串视为缺失
                if val_stripped == "":
                    missing_per_field[col] += 1
                    if col in detail_fields:
                        missing_detail[col].append(
                            (
                                total_rows,  # 当前是第几行（不含表头）
                                row.get("csvbase_row_id"),
                                row.get("title"),
                            )
                        )

                # 专门统计 title 缺失
                if col == "title" and val_stripped == "":
                    title_missing += 1

    # 输出结果
    print(f"文件: {src_path}")
    print(f"总行数（不含表头）: {total_rows}")
    print()
    print("1. title 缺失统计（为空或全是空白）：")
    print(f"   缺失行数: {title_missing}")
    if total_rows > 0:
        ratio = title_missing / total_rows * 100
        print(f"   缺失占比: {ratio:.2f}%")
    print()
    print("2. 各字段缺失统计（值为空字符串视为缺失）：")
    for col in fieldnames:
        miss = missing_per_field[col]
        if total_rows > 0:
            r = miss / total_rows * 100
            print(f"   {col}: {miss} 行缺失，占比 {r:.2f}%")
        else:
            print(f"   {col}: {miss} 行缺失")

    # 3. 重点字段缺失的具体行信息
    print()
    print("3. 重点字段缺失行（actors / language / studio）：")
    for col in ("actors", "language", "studio"):
        rows = missing_detail.get(col) or []
        if not rows:
            print(f"   字段 {col}: 无缺失行")
            continue
        print(f"   字段 {col}: 共 {len(rows)} 行缺失，前 50 行示例：")
        for line_no, rid, title in rows[:50]:
            print(f"     行 {line_no}: csvbase_row_id={rid}, title={title}")


if __name__ == "__main__":
    # 默认检查 movies_clean.csv，如需检查其他 CSV，可在命令行中调用函数或修改默认路径
    check_csv()

