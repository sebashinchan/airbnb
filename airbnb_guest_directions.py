#!/usr/bin/python

# This script creates a visual guide with walking directions from address A to address B (both supplied by the user)
# I envisioned this as a prototype of a tool that Airbnb hosts could use to generate directions for their guests.
# Airbnb hosts benefit from a consistent, accurate, and fast method of generating directions to their accomodation.
# Airbnb guests benefit from a consistent experience, and a reduced likelyhood of getting lost on their way to the accomodation.

# The output of this script is an JPG file that contains a series of streetview images from every step of the journey 
# between two points (based on Google Maps Directions API), as well as a text overlay that further describe the 
# route.

# I wrote this script after a trip to Japan, where an Airbnb host had sent me a PDF containing a very confusing set of directions.
# Sparse images and crudely drawn arrows (using MS Paint!) made it hard to follow, especially in a foreign country.
# I began to think of an automated way of generating directions that could be used offline, since phone data is not always available!

# Import Google Maps API client library, as well as libraries for helping to manipulate the API's response
import os, googlemaps, math, numpy as np, requests, urllib, json
from datetime import datetime

# #Import convert function in order to decode route polylines
from googlemaps import convert
# Import Pillow in order to edit and combine street view images
from PIL import Image, ImageDraw, ImageFont

#Get user's starting address and destination address
start = str(raw_input("From: "))
end = str(raw_input("To: "))

#Get the user to select a path to save the script's results
save_img_path = str(raw_input("Save directions to: "))

#Get the user to enter his/her API key in order to call Google Maps API.
api_key = str(raw_input("Enter your API key: "))
print("Please ensure you have enabled Google's Directions API and Street View Static API.")
raw_input("Press Enter to continue...")

#Define helper functions below

#Define funtion for parsing HTML directions returned in JSON response from Google Maps API
#This function remove HTML tags and does some minor formatting so that the text directions are human-friendly and easy to read.
#Function accepts a string containing HTML code 
def parse_html(html_string):
    #Identify HTML tag locations (range)
    html_tag_loc_list = []
    for i in range (0, len(html_string)):
        if html_string[i] == '<':
            for j in range(i,len(html_string)):
                if html_string[j] == '>':
                    html_tag_loc = [i,j]
                    html_tag_loc_list.append(html_tag_loc)
                    break
    
    #Create parsed text descriptions
    parsed_html_str = ''
    for j in range(0, len(html_tag_loc_list)):
        if j == 0:
            parsed_html_str = parsed_html_str + html_string[:html_tag_loc_list[j][0]]
        else:
            #Only keep strings that are outside of HTML tag locations
            #For example, if tags are found in ranges [5,10] and [17,20] (inclusive)...
            #...the string_to_add variable would assume the values [0,4] [11,16] and [21:]and add them to the parsed_html_str variable
            string_to_add = html_string[(html_tag_loc_list[j-1][1]+1):html_tag_loc_list[j][0]]
            #If no space exists at the end of the previously appended string, check whether the current string_to_add begins with a space
            if len(parsed_html_str)>0 and parsed_html_str[-1] != ' ':
                #If a space does not exist at the start of the string _to_add, Add comma and space between appended strings if none currently exist
                if len(string_to_add)>0 and string_to_add[0] != ' ':
                    parsed_html_str = parsed_html_str + ', ' + string_to_add
                #Else append string_to_add as is to total directions string
                else:
                    parsed_html_str = parsed_html_str + string_to_add
            #Else append string to total directions string
            else:
                parsed_html_str = parsed_html_str + string_to_add
    return parsed_html_str


# Create a function to calculate heading between two sets of lat/lng coordinates
# Coordinates are stored as tuples
# In order to perform the heading calculation I referenced a function from the following user: https://gist.github.com/jeromer/2005586
# Thank you kind stranger!
def calc_heading(pointA, pointB):

    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

# Create a function to convert a dictionary to tuple of coordinates
def convert_lat_lng_dict_to_tuple(dictA):

    tupleB = (dictA['lat'],dictA['lng'])

    return tupleB

# Create a function to add text to image; used to lay directions over corresponding street view image
# text_to_image function requires two arguments: 1) the image's file path and 2) the text to overlay onto the image
def text_to_image(image_path,text_to_add,page_num=False):
    # Open image
    image = Image.open(image_path)
    width, height = image.size
     
    draw = ImageDraw.Draw(image)
    text = text_to_add
    
    # Use Arial font, size 15 to write directions
    font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 15)
    textwidth, textheight = draw.textsize(text, font)

    # Calculate the x,y coordinates of where the text will be placed
    if page_num == False:
        x = (width - textwidth)/2
        y = height - textheight - 50
    else:
        x = (width - textwidth)/2
        y = height - textheight - 20
     
    # Place text on image at specified coordinates
    draw.text((x, y), text, font=font)
     
    # Save image to specified path
    image.save(image_path)


# Now the fun begins! 

# Authenticate the user's API key
gmaps = googlemaps.Client(key=api_key)

# Get the time for which we will be requesting directions
now = datetime.now()

# Request walking directions from starting address to destination address, leaving now
directions_result = gmaps.directions(start, end, mode="walking", departure_time=now)

# Isolate polyline from API's JSON response. A polyline is a representation of coordinates that form a walking path.
# Get each step of the polyline from JSON response. Each step will have a text direction associated with it e.g. "Turn left at Yonge St."
directions_steps  = directions_result[0]['legs'][0]['steps']

# For each step, get the encoded polyline. Level does not matter since Street View API will be called.
# Each point on the polyline will need to be decoded into a latitude/longitude pair.
# For each step, Google provides a written description (HTML) of the directions. Parse the directions into human-friendly text instructions.
directions_polylines = []
instructions = []
for j in range(0, len(directions_steps)):
    # Pull polyline for each step
    directions_polylines.append(directions_steps[j]['polyline']['points'])
    # Pull and parse HTML directions
    instructions.append(parse_html(str(directions_steps[j]['html_instructions'])))

# Decode polyline into tuple list of lat/lng coordindates
decode_coordinates = []
for polyline in directions_polylines:
    decode_coordinates.append(convert.decode_polyline(polyline))


# Calculate the bearing(i.e. heading, point of view) for every coordinate pair;
# GET request from Google Maps Street View API for each coordinate pair and the corresponding bearing.
# Calculating the bearing will ensure that we retrieve the correct image for the direction the user would be facing when following the directions.
bearing_list = []
request_url = 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location='
request_delim = ','
request_heading = '&heading='
request_url_metadata = 'https://maps.googleapis.com/maps/api/streetview/metadata?size=600x300&location='

# Fix the pitch (tilt of the viewer) so ensure that images are captured as if looking straight ahead.
request_pitch_api_key = '&pitch=-0.76&key='+api_key

page_seq = 1 # Keeping tracking of sequence will allow the images to be identified and placed in the correct order.
img_list = []

# Loop through each step of the route
for j in range(0,len(decode_coordinates)):
    # Loop through each coordinate pair (lat/lng) on the route's polyline
    for i in range(1,len(decode_coordinates[j])):
        
        # Starting point coordinates
        tupleCoordinates_start = convert_lat_lng_dict_to_tuple(decode_coordinates[j][i-1])
        # Ending point coordinates
        tupleCoordinates_end = convert_lat_lng_dict_to_tuple(decode_coordinates[j][i])
        # Heading for street view image
        # Heading is calculated as the direction from the starting lat/lng pair to the next lat/lng pair
        heading = calc_heading(tupleCoordinates_start,tupleCoordinates_end)
        
        # Convert coordinates and heading values to strings in order to make the Street View API request
        img_lat = str(tupleCoordinates_end[0])
        img_lng = str(tupleCoordinates_end[1])
        img_hdg = str(heading)
        
        # Create the API request for Street View image
        api_request_url = request_url+img_lat+request_delim+img_lng+request_heading+img_hdg+request_pitch_api_key
        # Create the API metadata requestn for Street View image
        api_request_url_metadata = request_url_metadata+img_lat+request_delim+img_lng+request_heading+img_hdg+request_pitch_api_key
        # GET Street View metadata
        r = requests.get(api_request_url_metadata)
        # Load metadata JSON response; metadata will allow us to detect wether the GET request for a streetview image was successful.
        img_metadata_response = r.json()
        
        # Check status of Street View API request
        response_status = img_metadata_response.get('status')
        # If the response is ok, save image to designated path, else print error message
        if response_status == 'OK':
            # Make the API request
            # Open and save retrieved image to personal folder
            urllib.urlretrieve(api_request_url, os.path.join(save_img_path,str(str(j)+'_'+str(i))+'_street_view.jpg'))
            img_path = save_img_path+'/'+str(str(j)+'_'+str(i))+'_street_view.jpg'
            if i == 1 :
            	# At the start of each step of the journey, add the text direction overtop of the image. This will ensure the user
            	# does not miss a turn.
                text_to_image(img_path,instructions[j])
            # Add sequence numbers to the images for further clarity.
            text_to_image(img_path,str(page_seq),True)
            img_list.append(img_path)   
        # Error handling:
        elif response_status in ['ZERO_RESULTS','NOT_FOUND']:
            print('Street view image not found!')
        else:
            print(response_status)
        page_seq = page_seq+1


# Vertically stack images into single image for user consumption
# This image can then be saved offline on the user's phone or printed for easy reference.
imgs = [Image.open(i) for i in img_list]

min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

imgs_comb = Image.fromarray( imgs_comb)
imgs_comb.save( save_img_path+'/Full_Directions.jpg' )  

# Remove individual images once directions have been created, leaving only the final, compiled set of directions.
for i in img_list:
    os.remove(i)

# The End