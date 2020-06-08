import ast
import tabulate

SVG_START = '<svg width="1000" height="1000">'
SVG_END = '</svg>'
MAIN_PATH = '<path d="{}" style="fill:none;stroke:#999999;stroke-width:5;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />'
FINAL_PATH = '<path d="{}" style="fill:none;stroke:#00FF00;stroke-width:5;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />'
START_POINT = '<circle cx="{}" cy="{}" r="10" fill="red" />'
END_POINT = '<circle cx="{}" cy="{}" r="10" fill="blue" />'
SUB_PATH = '<path d="{}" style="fill:none;stroke:#000000;stroke-width:2.52959;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />'
PATH_POINT = '<circle cx="{}" cy="{}" r="10" fill="black" />'
BLACK_PATH = '<path d="{}" style="fill:none;stroke:#000000;stroke-width:2.52959;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />'
RECT = '<rect x="0" y="0" width="1000" height="1000" fill="white" />'
MATRIX_TEXT = '<text x="{}" y="{}" fill="black" style="font-size: 14px;font-family: monospace;" xml:space="preserve">{}</text>'
BIG_TEXT = '<text x="{}" y="{}" fill="{}" style="font-size: 30px;font-familly: monospace;">{}</text>'

points = []
frame = {
}
max_delta = None
this_delta = None
final_curve = None
frame_count = 0
def generate_straight_path(points):
    string = ""
    MOVE_STRING = "M {},{} "
    LINE_STRING = "L {},{} "
    for i, point in enumerate(points):
        if i == 0:
            string += MOVE_STRING.format(point[0], point[1])
        else:
            string += LINE_STRING.format(point[0], point[1])
    return string

def generate_cubic(points):
    string = "M {},{} C {},{} {},{} {},{}"
    return string.format(points[0][0], points[0][1],
                         points[1][0], points[1][1],
                         points[2][0], points[2][1],
                         points[3][0], points[3][1])
def generate_frame(frame):
    global frame_count
    with open("frames-s/frame-{:02}.svg".format(frame_count), "w") as f:
        f.write(SVG_START)
        f.write(RECT)
        f.write(MAIN_PATH.format(generate_straight_path(points)))
        for point in points:
            f.write(PATH_POINT.format(point[0], point[1]))
        f.write(SUB_PATH.format(generate_cubic(frame["curve"])))
        f.write(START_POINT.format(frame["curve"][0][0], frame["curve"][0][1]))
        f.write(END_POINT.format(frame["curve"][3][0], frame["curve"][3][1]))
        best = frame["best"]
        table_str = tabulate.tabulate(best)
        y = 250
        for row in table_str.split('\n'):
            f.write(MATRIX_TEXT.format(290, y, row))
            y += 20
        f.write(BIG_TEXT.format(290, 600, "red", "start: " + frame["stP"]))
        f.write(BIG_TEXT.format(290, 650, "blue", "end: " + frame["enP"]))
        f.write(BIG_TEXT.format(290, 700, "green", "delta: " + frame["delta"]))
        if final_curve is not None:
            f.write(BIG_TEXT.format(290, 750, "red", "this_delta: {}".format(this_delta)))
            f.write(BIG_TEXT.format(290, 800, "blue", "max_delta: {}".format(max_delta)))
            f.write(FINAL_PATH.format(final_curve))
        f.write(SVG_END)
    frame_count += 1
with open("output.txt", "r") as f:
    for line in f:
        if line.find("points: ") == 0:
            point_string = line.replace("points: ", "").strip()
            points = ast.literal_eval(point_string)
        elif line.find("stP: ") == 0:
            stP = line.replace("stP: ", "").strip()
            frame["stP"] = stP
        elif line.find("enP: ") == 0:
            enP = line.replace("enP: ", "").strip()
            frame["enP"] = enP
        elif line.find("delta: ") == 0:
            delta = line.replace("delta: ", "").strip()
            frame["delta"] = delta
        elif line.find("Curve: ") == 0:
            curve = line.replace("Curve: ", "").strip()
            frame["curve"] = ast.literal_eval(curve)
        elif line.find("best: ") == 0:
            best = line.replace("best: ", "").strip()
            frame["best"] = ast.literal_eval(best)
            generate_frame(frame)
        elif line.find("Max Delta: ") == 0:
            max_delta_string = line.replace("Max Delta: ", "").strip()
            max_delta = float(max_delta_string)
        elif line.find("This delta: ") == 0:
            this_delta_string = line.replace("This delta: ", "").strip()
            this_delta = float(this_delta_string)
        elif line.find("final_curve: ") == 0:
            final_curve = line.replace("final_curve: ", "").strip()
generate_frame(frame)
