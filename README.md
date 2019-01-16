# Airbnb Guest Directions
Generate walking directions (with pictures!) for Airbnb guests.

This script creates a visual guide with walking directions from address A to address B (both supplied by the user). I envisioned this as a prototype of a tool that Airbnb hosts could use to generate directions for their guests. Airbnb hosts benefit from a consistent, accurate, and fast method of generating directions to their accomodation. Airbnb guests benefit from a consistent experience, and a reduced likelyhood of getting lost on their way to the accomodation.

The output of this script is an JPG file that contains a series of streetview images from every step of the journey 
between two points (based on Google Maps Directions API), as well as a text overlay that further describe the 
route.

I wrote this script after a trip to Japan, where an Airbnb host had sent me a PDF containing a very confusing set of directions. Sparse images and crudely drawn arrows (using MS Paint!) made it hard to follow, especially in a foreign country. I began to think of an automated way of generating directions that could be used offline, since phone data is not always available!
