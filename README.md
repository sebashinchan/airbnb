# Generating A Visual Guide Complete Directions for Airbnb Guests
Python script to generate walking directions (with pictures!) for Airbnb guests.

This script creates a visual guide with walking directions from address A to address B (both supplied by the user). I envisioned this as a prototype of a tool that Airbnb hosts could use to generate directions for their guests. Airbnb hosts benefit from a fast and reliable method of generating directions to their accomodation. Airbnb guests benefit from a consistent experience, and a reduced likelihood of getting lost on the way to their accomodation.

The output of this script is a JPG file that contains a series of streetview images from every step of the journey 
between two points (based on Google Maps Directions API), as well as text overlays that further describe the 
route.

I wrote this script after a trip to Japan, where an Airbnb host had sent me a PDF containing a very confusing set of directions. Sparse images and crudely drawn arrows (using MS Paint!) made it hard to follow, especially in a foreign country. I began to think of an automated way of generating directions that could be used offline, since phone data is not always available!

Below is a sample of the output of this script. The inputs were two addresses, 33 Bloor St. and 35 Hayden St. The result is a continuous image complete with text directions at each turn.
![sample image](https://lh3.googleusercontent.com/kB7xTWQ1qRpCrCzXZuN8jDtChc-D93chKIL6XehTluy5fbV16qk7RhK_wTG9EMGdMpbkCFE5bug-j-ZPvws9sqpFSqXNVeSXWXYPf7pLxXBjAHF0yxFS68jdjYVjUAPKk7HAiQezAiPWjKSwm8ZB4IZu8HBEN0TyXEL4SJtZZBZjMTeZCo2VOXDP7R3wd3iF5S5vyy_gReGJkPJQuNxW9KIMJiYomO4w5fN4UJ-DFtRVKfJwU10oPC98IWYb1z6fKa60NNPWjapuMl4PrUrMYiFQoajJLwxaSg72CIrCy5AAlnRJg__h19FE97lxVthYh0JIZdnLxHpLXAHsjfxD_E59gGfPyLeiNvNBfuz7k-FCqM-p7UYtuvdO8kwNnLGB7xcCOjQfwgJFhlZOwiiWa0bXuCVmWiKfGXmN61MZswQ7iJBK5E2nKwDicKo5813kbnf_ITTwuW-54cVO7k7ZmC_M7fFcBOOl_oyjpjIby2XsxXVOFjW6KYB2J8yMM3SQtkZqloUtsQ65F2biWaK0QtogXILWhMbLp1lPawUccFduieXs4Jn8MArW-JtE9FaMSf-n5us-7i1yvFQ2HGlghQ3raOptLPv6mvZ4BFq91HcykgNCC_VIhOdVoft46r0y42LH8VOuxuqwWbNu0x1kAgb7=w206-h1236-no)
