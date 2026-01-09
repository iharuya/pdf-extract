import argparse
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def extract_pages(input_path: Path, pages: list[int], output_path: Path) -> None:
    """指定されたページを抽出して新しいPDFを作成する"""
    reader = PdfReader(input_path)
    writer = PdfWriter()

    total_pages = len(reader.pages)

    for page_num in pages:
        if page_num < 1 or page_num > total_pages:
            raise ValueError(f"ページ {page_num} は範囲外です (1-{total_pages})")
        writer.add_page(reader.pages[page_num - 1])

    with open(output_path, "wb") as f:
        writer.write(f)


def parse_pages(pages_str: str) -> list[int]:
    """ページ指定文字列をパースする (例: "1,3,5-7" -> [1,3,5,6,7])"""
    pages = []
    for part in pages_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            pages.extend(range(int(start), int(end) + 1))
        else:
            pages.append(int(part))
    return pages


def main() -> None:
    parser = argparse.ArgumentParser(description="PDFからページを抽出する")
    parser.add_argument("input", type=Path, help="入力PDFファイル")
    parser.add_argument("-f", "--from", dest="from_page", type=int, help="開始ページ")
    parser.add_argument("-t", "--to", dest="to_page", type=int, help="終了ページ")
    parser.add_argument(
        "-p", "--pages", type=str, help="抽出するページ (例: 1,3,5-7)"
    )
    parser.add_argument("-o", "--output", type=Path, help="出力ファイル名")

    args = parser.parse_args()

    if not args.input.exists():
        print(f"エラー: 入力ファイル '{args.input}' が見つかりません", file=__import__("sys").stderr)
        raise SystemExit(1)

    if args.pages:
        pages = parse_pages(args.pages)
        default_output = f"{args.pages.replace(',', '_')}.pdf"
    elif args.from_page and args.to_page:
        pages = list(range(args.from_page, args.to_page + 1))
        default_output = f"{args.from_page}-{args.to_page}.pdf"
    elif args.from_page:
        pages = [args.from_page]
        default_output = f"{args.from_page}.pdf"
    else:
        parser.error("--from/--to または --pages を指定してください")

    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)

    output_path = out_dir / (args.output or Path(default_output))

    if output_path.exists():
        print(f"エラー: {output_path} は既に存在します", file=__import__("sys").stderr)
        raise SystemExit(1)

    extract_pages(args.input, pages, output_path)
    print(f"抽出完了: {output_path} ({len(pages)}ページ)")


if __name__ == "__main__":
    main()
