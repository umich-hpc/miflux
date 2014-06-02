
# Create the DMG background image

See https://developer.apple.com/library/mac/documentation/GraphicsAnimation/Conceptual/HighResolutionOSX/Optimizing/Optimizing.html#//apple_ref/doc/uid/TP40012302-CH7-SW13


Open the Pixelmator file, export the image as `dmg-background@2x.png`.  Make sure to save the Pixelmator file if you've been making changes to it.

Still in Pixelmator, resize the image to 800 pixels wide and export it again as `dmg-background.png`.  Close the image, being careful not to save it -- don't overwrite the original 1600 pixel wide Pixelmator file!

Combine the two .png files into a single .tiff file by running the following command:

```bash
tiffutil -cathidpicheck dmg-background.png dmg-background@2x.png \
  -out dmg-background.tiff
```
