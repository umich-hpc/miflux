
# Recreating the application icon

Download the U-M Block-M logo as PNG (the file will be named `BlockM-rball.png`) from
https://vpcomm.umich.edu/brand/downloads/um-logo
We're not including this file in the repository for intellectual property reasons.

To re-create the PDF of the surface integral symbol, run the following (this was done on Fedora 20, just because it was more expedient to install TeX there than under MacOS X).

```bash
sudo yum install texlive texlive-esint texlive-esint-type1
pdflatex surfint.tex
```

Open `surfint.pdf` in Apple Preview and zoom in on the symbol.  The exact size does not matter, but make it nice and big (minimum 1024 pixels vertically, larger is better).  Take a screenshot using Shift-Command-4 and rename the screenshot to `surfint.png`.

In [Pixelmator](http://www.pixelmator.com/) or a similar Photoshop-like program, open both `BlockM-rball.png` and `surfint.png`.

Create a new image named `miflux-icon-1024` that is 1024x1024 pixels (the largest icon size will be 512x512 at 2x retina resolution, or 1024x1024).  Set the background layer to transparent.

The Block M logo is 1000 pixels wide, not counting the (R) in the lower left.  Cut out the M, excluding the (R), scale it up to 1024 pixels wide, and paste it into a new layer in our new image, centering it horizontally and vertically.

In the `surfint.png` window, save (rename) it as a Pixelmator document named `surfint-with-glow.pxm`.  Use the Magic Eraser Tool to make the white background transparent in all areas of the image.  We'll need a couple hundred pixels of background on all sides of the symbol for the glow -- if there is not enough, increase the canvas size.

U-M Colors are described at
https://vpcomm.umich.edu/brand/style-guide/design-principles/colors
We don't want to use the primary U-M blue for the glow, as this is too close to the black of the surface integral symbol.  Instead, use the "Secondary, Bright" Blue named "Arboretum Blue", CMYK: C88 / M50 / Y0 / K0.

Add the glow effect to `surfint.pxm`:
* Edit -> Select Color -> Black
* Edit -> Refine Selection:
  * Size: 25px (assuming roughly a 1000px high image, adjust as necessary)
  * Feather: 40%
* Paint Bucket Tool -> Select Color CMYK 88/50/0/0, fill in the selection

Select and copy the area of the image that contains the integral and glow, paste this into a new image, then scale that image to be 1024 px vertically.  Select-all, copy, paste into a new layer in `miflux-logo-1024`.  Adjust the positioning so that the surface integral loop is centered over the Block M.

Save the file, and export to PNG as `milogo-icon-1024.png`.

Start [Icon Slate](http://www.kodlian.com/apps/icon-slate).  Open a new project and select the formats icns, iconset, and ico.

File -> Import Image -> `miflux-icon-1024.png`

File -> Rename -> `miflux-icon.iconsproj`

Click Build button.

