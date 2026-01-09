# pdf-extract

PDFからページを抽出するCLIツール

## 使い方

```bash
# ページ範囲を指定
uv run pdf-extract input.pdf --from 3 --to 5

# 個別のページを指定
uv run pdf-extract input.pdf --pages 1,3,5-7

# 出力ファイル名を指定
uv run pdf-extract input.pdf --from 1 --to 10 --output chapter1.pdf
```

## ページラベルモード (-l, --by-label)

PDFによっては、目次がローマ数字 (i, ii, iii, ...) で、本文がアラビア数字 (1, 2, 3, ...) のようにページラベルが設定されています。`-l` オプションを使うと、物理的なページ順ではなく、ラベルでページを指定できます。

```bash
# ラベル "1" のページを抽出（物理順ではなく、PDF内で "1" と表示されるページ）
uv run pdf-extract input.pdf -l -p 1

# ローマ数字のページを範囲指定
uv run pdf-extract input.pdf -l --from i --to x

# ローマ数字のページを個別指定
uv run pdf-extract input.pdf -l --pages i,iii,v
```
