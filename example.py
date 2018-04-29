import image_table
import pandas as pd
import openpyxl
from collections import OrderedDict


def usage1():
    # 1. DataFrame

    df = pd.read_csv("data.csv", names=["name", "path", "cat score"])
    df.insert(2, "image", df["path"])
    df = image_table.image_column(df, image_headers=["image"], escape_headers=["name"], image_width=200)

    data = df.to_html(
        classes=["table", "table-bordered", "table-hover"],
        escape=False,
        index=False
        )
    html = image_table.render_df(data, "templates/template_for_df.html")
    image_table.save_html(html, "test1.html")

    print("create test1.html")


def usage2():
    # 2. jinja2

    df = pd.read_csv("data.csv", names=["name", "path", "cat score"])
    df.insert(2, "image", df["path"])
    data = df.to_dict("records", into=OrderedDict)
    html = image_table.render_df(data, "templates/template.html")
    image_table.save_html(html, "test2.html")

    print("create test2.html")


def usage3():
    # 3. excel

    df = pd.read_csv("data.csv", names=["name", "path", "cat score"])
    df.insert(2, "image", df["path"])

    xl_path = "test3.xlsx"

    df.to_excel(xl_path, index=False)

    wb = openpyxl.load_workbook(xl_path)
    ws = wb.active
    image_table.image_column_xl(ws, "C")
    wb.save(xl_path)

    print(f"create {xl_path}")


if __name__ == "__main__":
    usage1()
    usage2()
    usage3()
