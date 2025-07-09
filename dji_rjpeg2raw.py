
import argparse
import os
import platform
import warnings
import shutil
from pathlib import Path
import numpy as np
import rasterio as rio
from rasterio.errors import NotGeoreferencedWarning
# from matplotlib import pyplot as plt

# Suppress the warning
warnings.filterwarnings("ignore", category=NotGeoreferencedWarning)

def call_tsdk(tsdk, input_path, output_path, label='T'):
    # conversion from DJI R-JPEG to RAW uint16 image
    # ./dji_irp.exe -s ../../../../dataset/H20T/DJI_0001_R.JPG -a extract -o extract.raw
    output_path.mkdir(parents=True, exist_ok=True)
        
    im_list = os.listdir(input_path)
    for im_name in im_list:
        if im_name.endswith('.JPG') or im_name.endswith('.jpg'):
            if label in im_name:
                rawfile_path = output_path / (im_name[:-4]+'.raw')
                if os.path.exists(rawfile_path):
                    continue  # skip if the raw file already exists
                try:                    
                    param = f'-s "{input_path}/{im_name}" -a extract -o "{rawfile_path}"'
                    os.system(f'{tsdk} {param}')
                except Exception as e:
                    print(f"Error converting R-JPEG to RAW {im_name}: {e}")
                    continue

def main(opt):
    
    output_path = opt.output_path
    output_path.mkdir(parents=True, exist_ok=True) 
    tmp_path = output_path.parent / 'raw16'
     
    # read the raw16 image
    for im_name in os.listdir(tmp_path):
        if im_name.endswith('.raw'):
            im_path = str(tmp_path / im_name)
            im = np.fromfile(im_path, dtype=np.uint16)
            im = im.reshape((opt.h, opt.w))  # reshape according to the DJI M3T R-JPEG image size    
            
            # save the image as a tiff file
            out_tif_path = output_path / (im_name[:-4] + '.tif')
            with rio.open(
                out_tif_path,
                'w',
                driver='GTiff',
                dtype='uint16',
                width=opt.w,
                height=opt.h,
                count=1,
                compress='lzw'
                ) as dst:
                dst.write(im, 1)
                            
            # write the exif data with exiftool
            im_tmp_path = opt.input_path / (im_name[:-4] + '.JPG')

            # -TagsFromFile: source file
            # -all: copy all tags
            # -overwrite_original: don't leave backup file
            try:
                param = f'-tagsfromfile "{im_tmp_path}" -all:all -overwrite_original "{out_tif_path}"'
                os.system(f'{opt.exiftool} {param}')
            except Exception as e:
                print(f"Error writing EXIF data for {im_name}: {e}")
                continue

def parse_opt(known=False): 
    parser = argparse.ArgumentParser() 
    parser.add_argument('--input_path', type=Path, required=True, help='Path to the input folder containing DJI R-JPEG images')
    parser.add_argument('--output_path', type=Path, required=True, help='Path to the output folder for TIFF images')
    parser.add_argument('--tsdk', type=str, help='Folder containing DJI Thermal SDK executable')
    parser.add_argument('--exiftool', type=str, help='Folder containing exiftool executable')
    parser.add_argument('--h', type=int, default=512, help='Height of the DJI R-JPEG image')
    parser.add_argument('--w', type=int, default=640, help='Width of the DJI R-JPEG image')
    parser.add_argument('--label', type=str, default='T', help='Label to filter the R-JPEG images')
    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt 
       
if __name__ == '__main__':
    opt = parse_opt(True)
    
    # check if the os is window or linux
    if platform.system() == 'Windows':
        tsdk = Path(opt.tsdk) / 'utility/bin/windows/release_x64/dji_irp.exe'
        opt.exiftool = Path(opt.exiftool) / 'exiftool.exe'
    else:   
        tsdk = Path(opt.tsdk) / 'utility/bin/linux/release_x64/dji_irp'
        opt.exiftool = "perl " + str(Path(opt.exiftool) / 'exiftool')
        
    tmp_path = opt.output_path.parent / 'raw16'
    # conversion from DJI M3T R-JPEG to RAW16 image
    call_tsdk(tsdk, opt.input_path, tmp_path, label=opt.label)    
       
    main(opt)
    print("Conversion completed.")
    
    if tmp_path.exists():
        shutil.rmtree(tmp_path)  # remove the temporary raw16 folder
    print(f"TIFF images are saved in: {Path(opt.output_path).resolve()}")
