from pathlib import Path

import tifffile as tif


def read_tif(file=None):
    """Read tiff files. Works with 16 bit rgb data"""

    if file is not None:
        img = tif.imread(file)
        return img

    else:
        print("No file provided")


def write_tif(data=None, out_dir=".", file="test.tif"):
    """Write tiff files. Works with 16 bit rgb data"""

    if data is not None:
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        tif.imwrite(f"{out_dir}/{file}", data, photometric="rgb")

    else:
        print("No data provided")


img = read_tif(file="2020-09-03-1601_5-2020-09-03-1601_4-U-L-Mars_pipp_AS_F4000_lapl4_ap42_Drizzle15.tif")

write_tif(img, file="t2.tif")
