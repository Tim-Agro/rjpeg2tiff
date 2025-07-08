This repository provides a tool to convert DJI R-JPEG (Radiometric JPEG) thermal images into 16-bit TIFF files. The output (single-band TIFF) could be used for further analysis or photogrammetric processing (e.g., in Agisoft Metashape, Pix4D, etc.).

## 🔧 Installation of the required Python packages
```bash
pip install rasterio
```
## 📁 Sample data
Sample R-JPEG data is available from the repository [dji_h20t_rpeg_to_tif](https://github.com/tejakattenborn/dji_h20t_rpeg_to_tif/tree/main/sample_data).


## 📥 Required tools
### DJI thermal SDK
1. Download the TSDK (DJI Thermal SDK) from the [official DJI site](https://www.dji.com/nl/downloads/softwares/dji-thermal-sdk).
1. Unzip the TSDK into your project folder (the folder where you have cloned or forked this repository).
- *Note: by default, the `release_x64` build is used.*

    > On Linux: <br>
    > Before running the Python scripts to convert the R-JPEG to 16-bit TIFF, add  the directory containing `dji_irp` to your library path:
    >```bash
    > export LD_LIBRARY_PATH="/path/to/utility/bin/linux/release_x64:${LD_LIBRARY_PATH}"
    >```
    > Replace `/path/to/utility/bin/linux/release_x64` with the actual path where `dji_irp` resides.

### ExifTool
1. Download the [exiftool](https://exiftool.org/).
1. Unzip into your project folder.
   
   > On Windows: <br>
   > To enable command-line usage, rename `exiftool(-k).exe` to `exiftool.exe`.

## 🔄 Converting R-JPEG to 16-bit TIFF
Run the script using the following command:
```bash
python dji_rjpeg2raw.py --input_path input_path \
                        --output_path output_path \
                        --tsdk task_directory \
                        --exiftool exiftool_directory
```
🛠️ Optional arguments
- `--h`: Height of the DJI R-JPEG image
- `--w`: Width of the DJI R-JPEG image
- `--label`: Filter input files by filename label. Only the R-JPEG images containing this label will be processed. Default: `'T'` (filters for files such as `0001_T.JPG`)
> *A corresponding \*.raw file is temporarily saved in a `raw16` folder located in the parent directory of the output path. After processing, the `raw16` folder is automatically removed.*    
> *The EXIF metadata from the R-JPEG file is preserved and embedded in the output TIFF file.*

<br>

*Comparison of the original R-JPEG image and the converted TIFF image*
<img src="https://github.com/Tim-Agro/rjpeg2tiff/blob/main/image/rjpeg_vs_tiff.png" alt="img_title" width="750"/>
<br>

## 🗺️ Generating orthomosaic in Agisoft Metashape
For detailed instructions, please refer to [thermal imagery processing tutorial](https://agisoft.freshdesk.com/support/solutions/articles/31000158942-thermal-imagery-processing).
