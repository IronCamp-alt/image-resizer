import os
import sys
from PIL import Image
import cairosvg
from dxfwrite import DXFEngine as dxf

def resize_image(input_image_path, output_image_path, size):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(size)
    resized_image.save(output_image_path)

def convert_to_svg(input_image_path, output_svg_path):
    cairosvg.svg2png(url=input_image_path, write_to=output_svg_path)

def convert_to_eps(input_image_path, output_eps_path):
    image = Image.open(input_image_path)
    image.save(output_eps_path, 'EPS')

def convert_to_dxf(input_image_path, output_dxf_path):
    image = Image.open(input_image_path).convert('1')
    drawing = dxf.drawing(output_dxf_path)
    for y, row in enumerate(image.getdata()):
        for x, pixel in enumerate(row):
            if not pixel:
                drawing.add(dxf.point((x, y)))
    drawing.save()

def main(input_folder, output_folder, template_size):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                filename, ext = os.path.splitext(file)

                # Resize image
                resized_image_path = os.path.join(output_folder, f"{filename}_resized{ext}")
                resize_image(file_path, resized_image_path, template_size)

                # Save in different formats
                convert_to_svg(resized_image_path, os.path.join(output_folder, f"{filename}_resized.svg"))
                convert_to_eps(resized_image_path, os.path.join(output_folder, f"{filename}_resized.eps"))
                convert_to_dxf(resized_image_path, os.path.join(output_folder, f"{filename}_resized.dxf"))
                os.rename(resized_image_path, os.path.join(output_folder, f"{filename}_resized.png"))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python resize_and_convert.py input_folder output_folder template_size")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    template_size = tuple(map(int, sys.argv[3].split('x')))

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    main(input_folder, output_folder, template_size)
