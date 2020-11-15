#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import base64
from pathlib import Path
import os

def embed_svg_images(filename_in: Path, overwrite: bool = True):
    filename_in = Path(filename_in).resolve()
    filename_out = f'{filename_in.with_suffix("")}.b64.svg'
    images_b64 = {}  # cache base-64 encoded images
    num_images = 0   # just for debugging
    re_xlink=re.compile(r"xlink:href=\"(?P<URL>.*?)\"", re.IGNORECASE)
    with open(filename_in) as file_in, open(filename_out,'w') as file_out:
        for line in file_in:
            for xlink in re_xlink.finditer(line):
                num_images = num_images + 1
                imgurl = xlink.group('URL')
                if not imgurl in images_b64:
                    if not Path(imgurl).is_absolute():  # resolve relative image path
                        imgurl_abs = (Path(filename_in).parent / imgurl).resolve()
                    else:
                        imgurl_abs = imgurl

                    with open(imgurl_abs, 'rb') as img:
                        data_bin = img.read()
                        data_b64 = base64.b64encode(data_bin)
                        data_str = data_b64.decode('utf-8')
                    images_b64[imgurl] = data_str

                line = line.replace(imgurl,
                                    f'data:image/png;base64, {images_b64[imgurl]}')
            file_out.write(line)

        if overwrite:
            os.remove(filename_in)
            os.rename(filename_out, filename_in)
