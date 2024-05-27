# Polyfrac

A simple Python program that generates fractal regular polygons using configurable variables and color palettes.

# Screenshots

Hover for side count, fraction[^1], and smoothness[^2].

<p float="left">
    <img src="/a.png" title="6 sides, fraction 0.99131, smoothness 5, default palette" width="200">
    <img src="/b.png" title="4 sides, fraction 0.5, smoothness 0, default palette" width="200">
    <img src="/c.png" title="11 sides, fraction 0.05509, smoothness 3, default palette" width="200">
</p>

# Configuration

The palette can be configured by changing the RGB hex values in `palette.txt`, and the controls are as follows:

|key|effect|
|--|--|
|q|decrease side count by 1|
|w|increase side count by 1|
|a|decrease fraction[^1] while held down|
|s|increase fraction while held down|
|z|decrease smoothness[^2] by 1|
|x|increase smoothness by 1|
|e|save a screenshot|

[^1]: a value from 0-1 from which the next inner polygon starts (scaled up to the length of the outer polygon)
[^2]: how smooth the color palette is - zero is the normal palette, and each increase of 1 after that doubles the size by averaging neighbors

