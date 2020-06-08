SVG_START = '<svg width="1000" height="1000">'
SVG_END = '</svg>'
MAIN_PATH = '<path d="{}" style="fill:none;stroke:#999999;stroke-width:5;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />'
START_POINT = '<circle cx="{}" cy="{}" r="10" fill="red" />'
END_POINT = '<circle cx="{}" cy="{}" r="10" fill="blue" />'
SUB_PATH = '<path d="{}" style="fill:none;stroke:#000000;stroke-width:2.52959;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />'
PATH_POINT = '<circle cx="{}" cy="{}" r="10" fill="black" />'
BLACK_PATH = '<path d="{}" style="fill:none;stroke:#000000;stroke-width:2.52959;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />'
RECT = '<rect x="0" y="0" width="1000" height="1000" fill="white" />'

in_simplify = False
in_frame = False
points = []
frame = {
}
frame_count = 0
def generate_path(points):
    string = ""
    MOVE_STRING = "M {},{} "
    LINE_STRING = "L {},{} "
    for i, point in enumerate(points):
        if i == 0:
            string += MOVE_STRING.format(point[0], point[1])
        else:
            string += LINE_STRING.format(point[0], point[1])
    return string
def generate_frame(frame):
    global frame_count
    with open("frames/frame-{:02}.svg".format(frame_count), "w") as f:
        f.write(SVG_START)
        f.write(RECT)
        f.write(MAIN_PATH.format(frame["d"]))
        f.write(SUB_PATH.format(frame["sd"]))
        for point in points:
            f.write(PATH_POINT.format(point[0], point[1]))
        f.write(BLACK_PATH.format(generate_path(points)))
        f.write(START_POINT.format(frame["start"][0], frame["start"][1]))
        f.write(END_POINT.format(frame["end"][0], frame["end"][1]))
        f.write(SVG_END)
    frame_count += 1
with open("output.txt", "r") as f:
    for line in f:
        if line.find("d: ") == 0:
            path_string = line.replace("d: ", "").strip()
            in_simplify = True
            frame["d"] = path_string
        elif line.find("sd: ") == 0:
            subpath_string = line.replace("sd: ", "").strip()
            if in_frame == True:
                generate_frame(frame)
            in_frame = True
            frame["sd"] = subpath_string
        elif line.find("start: ") == 0:
            point = line.replace("start: ", "")
            x, y = point.split(',')
            x = float(x)
            y = float(y)
            frame["start"] = [x, y]
        elif line.find("end: ") == 0:
            point = line.replace("end: ", "")
            x, y = point.split(',')
            x = float(x)
            y = float(y)
            frame["end"] = [x, y]
        elif line.find("added: ") == 0:
            point = line.replace("added: ", "")
            x, y = point.split(',')
            x = float(x)
            y = float(y)
            points.append([x, y])
            frame["points"] = points
if in_frame == True:
    generate_frame(frame)
    in_frame = False
