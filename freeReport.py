from index import find_planets
from panchang import calculate_panchang

def freeReport(dob,location,lat,lon,path,gender,name,timezone):
    planets = find_planets(dob,lat,lon,timezone)
    panchang = calculate_panchang(dob,planets[2]['full_degree'],planets[1]['full_degree'],lat,lon)
    
    return {
        "planets": planets,
        "panchang": panchang,
    }
    