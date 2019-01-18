# Generating A Visual Guide Complete With Directions for Airbnb Guests

Hello there! I have written a small Python script to generate walking directions (with pictures!) for Airbnb guests that can used offline.

This script creates a visual guide with walking directions from address A to address B (both supplied by the user). I envisioned this as a prototype of a tool that Airbnb hosts could use to generate directions for their guests. Airbnb hosts benefit from a fast and reliable method of generating directions to their accomodation. Airbnb guests benefit from a consistent experience, and a reduced likelihood of getting lost on the way to their accommodation.

The output of this script is a JPG file that contains a series of streetview images from every step of the journey 
between two points (based on Google Maps Directions API), as well as text overlays that further describe the 
route.

I wrote this script after a trip to Japan, where an Airbnb host had sent me a PDF containing a very confusing set of directions. Sparse images and crudely drawn arrows (using MS Paint!) made it hard to follow, especially in a foreign country. I began to think of an automated way of generating directions that could be used offline, since phone data is not always available!

Below is a sample of the output of this script. The inputs were two addresses, 33 Bloor St. and 35 Hayden St. The result is a continuous image complete with text directions at each turn.

![sample image](https://i.imgur.com/pzVSNBM.jpg)
