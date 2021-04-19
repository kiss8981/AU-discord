from PIL import Image, ImageDraw, ImageFont


def generate_emoji(text, name, fonttype="NanumGothicBold.ttf", fontsize=64):

    # Specify TrueType font and Fontsize
    image = Image.new("RGBA", (128, 128), (255, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    if len(text) == 1:
        font = ImageFont.truetype(fonttype, size=120)
        draw.text((5, -7), "{}".format(text[0]), font=font, fill="#fff")
        image.save(f"emoji/{name}.png", "PNG")
    elif len(text) == 2:
        font = ImageFont.truetype(fonttype, size=70)
        draw.text((-2, 20), "{}".format(text[0:2]), font=font, fill="#fff")
        image.save(f"emoji/{name}.png", "PNG")
    elif len(text) == 3:
        font = ImageFont.truetype(fonttype, size=62)
        draw.text((1, -5), "{}\n  {}".format(text[0:2], text[2:3]), font=font, fill="#fff")
        image.save(f"emoji/{name}.png", "PNG")
    elif len(text) == 4:
        font = ImageFont.truetype(fonttype, fontsize)
        draw.text((0, 0), "{}\n{}".format(text[0:2], text[2:4]), font=font, fill="#fff")
        image.save(f"emoji/{name}.png", "PNG")