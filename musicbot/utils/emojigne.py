from PIL import Image, ImageDraw, ImageFont


def generate_emoji(text, name, fonttype: str = None, fontcolor: str = None, fontsize=64):


    if fonttype == None:
        fonttype = "NanumGothicBold.ttf"
    elif fonttype == "1":
        fonttype = "GmarketSansTTFBold.ttf"
    elif fonttype == "2":
        fonttype = "Jalnan.ttf"
    elif fonttype == "3":
        fonttype = "Cafe24Danjunghae.ttf"

    if fontcolor == None:
        fontcolor == "#fff"
    elif fontcolor == "노란":
        fontcolor = "#fffc00"
    elif fontcolor == "하늘":
        fontcolor = "#57ffdd"
    elif fontcolor == "핑크":
        fontcolor = "#ff9fcc"
    elif fontcolor == "빨강":
        fontcolor = "#ff0000"
    elif fontcolor == "보라":
        fontcolor = "#c6c6ff"
    elif fontcolor == "민트":
        fontcolor = "#c6faff"
    elif fontcolor == "연두":
        fontcolor = "#ceffc6"
    elif fontcolor == "주황":
        fontcolor = "#ffaa3b"

    image = Image.new("RGBA", (128, 128), (255, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    if len(text) == 1:
        font = ImageFont.truetype(fonttype, size=120)
        draw.text((5, -7), "{}".format(text[0]), font=font, fill=fontcolor)
        image.save(f"emoji/{name}.png", "PNG")
    elif len(text) == 2:
        font = ImageFont.truetype(fonttype, size=70)
        draw.text((-2, 20), "{}".format(text[0:2]), font=font, fill=fontcolor)
        image.save(f"emoji/{name}.png", "PNG")
    elif len(text) == 3:
        font = ImageFont.truetype(fonttype, size=62)
        draw.text((1, -5), "{}\n  {}".format(text[0:2], text[2:3]), font=font, fill=fontcolor)
        image.save(f"emoji/{name}.png", "PNG")
    elif len(text) == 4:
        font = ImageFont.truetype(fonttype, fontsize)
        draw.text((0, 0), "{}\n{}".format(text[0:2], text[2:4]), font=font, fill=fontcolor)
        image.save(f"emoji/{name}.png", "PNG")