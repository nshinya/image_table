import pandas as pd
from jinja2 import Template, Environment, FileSystemLoader, select_autoescape
import html
from collections import OrderedDict
import openpyxl
from openpyxl.drawing.image import Image


def image_column(df, image_headers=None, escape_headers=None, image_width=300):
    for header in image_headers:
        df[header] = df[header].map(lambda s: f"<img src='{s}' width='{image_width}' />")

    if escape_headers is not None:
        for header in escape_headers:
            df[header] = df[header].map(lambda s: html.escape(s))

    return df


def render_df(data, template_filename):
    env = Environment(loader=FileSystemLoader("."), autoescape="html")
    tmpl = env.get_template(template_filename)
    html = tmpl.render(data=data).encode("utf8")
    return html


def save_html(html, filename):
    with open(filename, "wb") as f:
        f.write(html)


def image_column_xl(worksheet, image_column, image_width=300):
    ws = worksheet

    # get row number
    R_NUM = len(list(ws.rows))

    # insert images
    for i in range(1, R_NUM):
        idx = i + 1
        cell_name = image_column + str(idx)
        c = ws[cell_name]
        try:
            # load the image file
            img = Image(c.value)
            # change the image width
            aspect = float(img.height) / img.width
            img.width = image_width
            img.height = aspect * image_width
            # paste the image
            ws.add_image(img, cell_name)
            # adjust cell size
            ws.row_dimensions[idx].height = img.height
            c.value = ""
        except FileNotFoundError:
            pass

    # adjust cell width
    ws.column_dimensions[image_column].width = image_width / 6


def usage1():
    # 1. DataFrame

    df = pd.read_csv("data.csv", names=["name", "path", "cat score"])
    df.insert(2, "image", df["path"])
    df = image_column(df, image_headers=["image"], image_width=300)

    data = df.to_html(
        classes=["table", "table-bordered", "table-hover"],
        columns=["name", "path", "image"],
        escape=False
        )
    html = render_df(data, "templates/template_for_df.html")
    save_html(html, "test1.html")


def usage2():
    # 2. jinja2

    df = pd.read_csv("data.csv", names=["name", "path", "cat score"])
    df.insert(2, "image", df["path"])
    data = df.to_dict("records", into=OrderedDict)
    html = render_df(data, "templates/template.html")
    save_html(html, "test2.html")


def usage3():
    # 3. excel

    df = pd.read_csv("data.csv", names=["name", "path", "cat score"])
    df.insert(2, "image", df["path"])

    xl_path = "test3.xlsx"

    df.to_excel(xl_path, index=False)

    wb = openpyxl.load_workbook(xl_path)
    ws = wb.active
    image_column_xl(ws, "C")
    wb.save(xl_path)


if __name__ == "__main__":
    usage1()
    usage2()
    usage3()
