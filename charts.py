# from datetime import datetime, timedelta
# import pytz
# import logging
# import swisseph as swe
# from geopy.geocoders import Nominatim
# from collections import defaultdict

# # data altering
# def to_jd_ut(birth_date, birth_time, timezone_pytz):
#     # Convert birth date and time to UTC
#     if isinstance(birth_date, str): 
#         birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
#     else:
#         time_object = datetime.strptime(birth_time, "%H:%M").time()
#         birth_datetime = datetime.combine(birth_date, time_object)
#     local_timezone = pytz.timezone(timezone_pytz)  # Replace with the correct timezone
#     birth_datetime = local_timezone.localize(birth_datetime)
#     birth_datetime_utc = birth_datetime.astimezone(pytz.utc)

#     # Calculate Julian Day for the birth date and time
#     jd_ut = swe.julday(birth_datetime_utc.year, birth_datetime_utc.month, 
#                           birth_datetime_utc.day, birth_datetime_utc.hour + 
#                           (birth_datetime_utc.minute / 60)) 
#     return jd_ut


# # 计算宫位


# # 计算各点
# points = {
#     "北交": swe.calc(jd, swe.MEAN_NODE)[0],
#     "婚神": swe.calc(jd, swe.JUNO)[0],
#     "上升": houses[0],
#     "中天": houses[9],
#     "金星": swe.calc(jd, swe.VENUS)[0]
# }

# # 计算福点
# sun = swe.calc(jd, swe.SUN)[0]
# moon = swe.calc(jd, swe.MOON)[0]
# points["福点"] = (points["上升"] + moon[0] - sun[0]) % 360

# # 输出结果
# for name, pos in points.items():
#     if isinstance(pos, tuple):
#         pos = pos[0]
#     zodiac = get_zodiac_sign(pos)
#     house = get_house(pos, houses)
#     print(f"{name}: {pos:.2f}度 {zodiac} 第{house}宫")


# # dates
# def get_solar_return (jd_birth, birth_date, year):

#     # Get natal Sun position
#     natal_sun_position = swe.calc_ut(jd_birth, swe.SUN)[0][0]

#     birth_datetime = datetime.strptime(f"{birth_date}", "%Y-%m-%d")

#     # Find the Solar Return
#     for day in range(365):  # Check each day of the year
#         jd = swe.julday(year, birth_datetime.month, birth_datetime.day + day, 0)
#         sun_position = swe.calc_ut(jd, swe.SUN)[0][0]
#         if sun_position >= natal_sun_position:
#             # Approximate time of Solar Return
#             solar_return_time = jd
#             break
#     return solar_return_time



# def get_lunar_return(natal_info, start_date):
#     natal_moon_deg = natal_info['MOON']['d']  # Access the 'd' key for degrees
#     zodiac_order = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
#                     'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    
#     # Convert natal degree to 360° format
#     natal_moon_long = zodiac_order.index(natal_info['MOON']['z']) * 30 + natal_moon_deg

#     # Function to find next Moon return
#     def find_moon_return(start_date, natal_moon_long):
#         date = datetime.strptime(start_date, "%Y-%m-%d")
#         init_year = date.year
#         counter = 0
#         marker = 1
#         dates = []
#         while date.year <= init_year:
#             jd = swe.julday(date.year, date.month, date.day)
#             transiting_moon = swe.calc_ut(jd, swe.MOON)[0][0]
#             if round(transiting_moon, 6) < round(natal_moon_long, 6) and marker == 1:
#                 marker = 0
#             elif round(transiting_moon, 6) >= round(natal_moon_long, 6) and marker == 0: 
#                 marker = 1
#                 dates.append(date.strftime("%Y-%m-%d"))
#                 counter += 1
#             else: 
#                 pass
#             date += timedelta(days=1)
#         return dates

#     # Find next Moon return
#     moon_return_date = find_moon_return(start_date, natal_moon_long)
#     return moon_return_date

# # house info
# # def astro_charts(jd_ut, latitude, longitude):
# #     try:
# #         planet_names = ["SUN", "MOON", "MERCURY", "VENUS", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE", "PLUTO"]
# #         zodiac_dict = {
# #             0: 'Aries', 1: 'Taurus', 2: 'Gemini', 3: 'Cancer', 4: 'Leo', 5: 'Virgo',
# #             6: 'Libra', 7: 'Scorpio', 8: 'Sagittarius', 9: 'Capricorn', 10: 'Aquarius', 11: 'Pisces'
# #         }
# #         zodiac_index = {sign: index for index, sign in zodiac_dict.items()}

# #         planets = {}
# #         for i, name in enumerate(planet_names):
# #             logging.debug(f"Calculating position for {name}")
# #             calc_result = swe.calc_ut(jd_ut, i)
# #             if calc_result[0] is None:
# #                 raise ValueError(f"Failed to calculate position for {name}")
# #             pos = calc_result[0][0]
# #             planets[name] = {
# #                 "d": round(pos % 30, 1),
# #                 "z": zodiac_dict[int(pos / 30)]
# #             }

# #         logging.debug(f"Calculating houses for jd_ut={jd_ut}, lat={latitude}, lon={longitude}")
# #         house_cusps, ascmc = swe.houses(jd_ut, latitude, longitude, b'P')
# #         if house_cusps is None or ascmc is None:
# #             raise ValueError("Failed to calculate houses")

# #         house_positions = {}
# #         for i in range(12):
# #             next_cusp = house_cusps[(i + 1) % 12]
# #             for planet, data in planets.items():
# #                 pos = data["d"] + (30 * zodiac_index[data["z"]])
# #                 if (pos >= house_cusps[i] and pos < next_cusp) or (i == 11 and (pos >= house_cusps[11] or pos < house_cusps[0])):
# #                     house_positions[planet] = i + 1

# #         chart_info = {
# #             planet: {
# #                 "h": house_positions.get(planet, 0),
# #                 "z": planets[planet]["z"],
# #                 "d": planets[planet]["d"]
# #             } for planet in planet_names
# #         }

# #         asc_info = {
# #             "z": zodiac_dict[int(ascmc[0] / 30)],
# #             "d": round(ascmc[0] % 30, 1)
# #         }

# #         return chart_info, asc_info

# #     except Exception as e:
# #         logging.error(f"Error in astro_charts: {str(e)}")
# #         raise


# import swisseph as swe
# import logging

# def astro_charts(jd_ut, latitude, longitude):
#     try:
#         planet_names = ["SUN", "MOON", "MERCURY", "VENUS", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE", "PLUTO"]
#         additional_points = ["NORTH_NODE", "JUNO", "MIDHEAVEN", "PART_OF_FORTUNE"]
#         zodiac_dict = {
#             0: 'Aries', 1: 'Taurus', 2: 'Gemini', 3: 'Cancer', 4: 'Leo', 5: 'Virgo',
#             6: 'Libra', 7: 'Scorpio', 8: 'Sagittarius', 9: 'Capricorn', 10: 'Aquarius', 11: 'Pisces'
#         }
#         zodiac_index = {sign: index for index, sign in zodiac_dict.items()}

#         planets = {}
#         for i, name in enumerate(planet_names):
#             logging.debug(f"Calculating position for {name}")
#             calc_result = swe.calc_ut(jd_ut, i)
#             if calc_result[0] is None:
#                 raise ValueError(f"Failed to calculate position for {name}")
#             pos = calc_result[0][0]
#             planets[name] = {
#                 "d": round(pos % 30, 1),
#                 "z": zodiac_dict[int(pos / 30)]
#             }

#         logging.debug(f"Calculating houses for jd_ut={jd_ut}, lat={latitude}, lon={longitude}")
#         house_cusps, ascmc = swe.houses(jd_ut, latitude, longitude, b'P')
#         if house_cusps is None or ascmc is None:
#             raise ValueError("Failed to calculate houses")

#         # Calculate additional points
#         north_node = swe.calc_ut(jd_ut, swe.MEAN_NODE)[0][0]
#         juno = swe.calc_ut(jd_ut, swe.JUNO)[0][0]
#         midheaven = ascmc[1]
#         sun_pos = planets["SUN"]["d"] + (30 * zodiac_index[planets["SUN"]["z"]])
#         moon_pos = planets["MOON"]["d"] + (30 * zodiac_index[planets["MOON"]["z"]])
#         asc_pos = ascmc[0]
#         part_of_fortune = (asc_pos + moon_pos - sun_pos) % 360

#         additional_points_data = {
#             "NORTH_NODE": north_node,
#             "JUNO": juno,
#             "MIDHEAVEN": midheaven,
#             "PART_OF_FORTUNE": part_of_fortune
#         }

#         for name, pos in additional_points_data.items():
#             planets[name] = {
#                 "d": round(pos % 30, 1),
#                 "z": zodiac_dict[int(pos / 30)]
#             }

#         house_positions = {}
#         for i in range(12):
#             next_cusp = house_cusps[(i + 1) % 12]
#             for planet, data in planets.items():
#                 pos = data["d"] + (30 * zodiac_index[data["z"]])
#                 if (pos >= house_cusps[i] and pos < next_cusp) or (i == 11 and (pos >= house_cusps[11] or pos < house_cusps[0])):
#                     house_positions[planet] = i + 1

#         chart_info = {
#             planet: {
#                 "h": house_positions.get(planet, 0),
#                 "z": planets[planet]["z"],
#                 "d": planets[planet]["d"]
#             } for planet in planet_names + additional_points
#         }

#         asc_info = {
#             "z": zodiac_dict[int(ascmc[0] / 30)],
#             "d": round(ascmc[0] % 30, 1)
#         }

#         return chart_info, asc_info, additional_points

#     except Exception as e:
#         logging.error(f"Error in astro_charts: {str(e)}")
#         raise


# def format_chart_data(chart):
#     return {planet: {"h": data["h"], "z": data["z"], "d": round(data["d"], 1)} 
#             for planet, data in chart.items()}

# # generate 1 year worth of info
# def get_yearly_info(year, timezone_pytz, latitude, longitude, natal_info, birth_date, birth_time):
#     y_str = str(year)
#     solar_return_jd = get_solar_return(to_jd_ut(birth_date, birth_time, timezone_pytz), birth_date, year)
#     solar_return, _ = astro_charts(solar_return_jd, latitude, longitude)
    
#     y_date = f"{y_str}-01-01"
#     lunar_return_dates = get_lunar_return(natal_info, y_date)
    
#     years_dict = {
#         y_str: {
#             "SR": {
#                 "info": "Solar Return chart",
#                 "chart": solar_return  # No need to format, astro_charts now returns the correct structure
#             },
#             "LR": {
#                 "info": "Lunar Return charts",
#                 "returns": []
#             }
#         }
#     }
    
#     for date in lunar_return_dates:
#         lunar_return, _ = astro_charts(to_jd_ut(date, "00:00", timezone_pytz), latitude, longitude)
#         years_dict[y_str]["LR"]["returns"].append({
#             "date": date,
#             "chart": lunar_return  # No need to format, astro_charts now returns the correct structure
#         })
    
#     return years_dict

# # generate 2 year worth of info
# def get_biyearly_info(year, timezone_pytz, latitude, longitude, natal_info, birth_date, birth_time):
#     years = [year, year + 1]
#     years_dict = {}
   
#     for y in years:
#         y_str = str(y)
#         y_date = f"{y_str}-01-01"
        
#         solar_return_jd = get_solar_return(to_jd_ut(birth_date, birth_time, timezone_pytz), birth_date, y)
#         solar_return, _ = astro_charts(solar_return_jd, latitude, longitude)
        
#         lunar_return_dates = get_lunar_return(natal_info, y_date)
        
#         years_dict[y_str] = {
#             "SR": {
#                 "info": "Solar Return chart",
#                 "chart": solar_return  # astro_charts now returns the correct structure
#             },
#             "LR": {
#                 "info": "Lunar Return charts",
#                 "returns": []
#             }
#         }
        
#         for date in lunar_return_dates:
#             lunar_return, _ = astro_charts(to_jd_ut(date, "00:00", timezone_pytz), latitude, longitude)
#             years_dict[y_str]["LR"]["returns"].append({
#                 "date": date,
#                 "chart": lunar_return  # astro_charts now returns the correct structure
#             })
    
#     logging.debug(f"Biyearly dict structure: {years_dict}")
#     return years_dict



from datetime import datetime, timedelta
import pytz
import logging
import swisseph as swe
from geopy.geocoders import Nominatim
from collections import defaultdict

# data altering
def to_jd_ut(birth_date, birth_time, timezone_pytz):
    # Convert birth date and time to UTC
    if isinstance(birth_date, str): 
        birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
    else:
        time_object = datetime.strptime(birth_time, "%H:%M").time()
        birth_datetime = datetime.combine(birth_date, time_object)
    local_timezone = pytz.timezone(timezone_pytz)  # Replace with the correct timezone
    birth_datetime = local_timezone.localize(birth_datetime)
    birth_datetime_utc = birth_datetime.astimezone(pytz.utc)

    # Calculate Julian Day for the birth date and time
    jd_ut = swe.julday(birth_datetime_utc.year, birth_datetime_utc.month, 
                          birth_datetime_utc.day, birth_datetime_utc.hour + 
                          (birth_datetime_utc.minute / 60)) 
    return jd_ut

def get_zodiac_sign(degree):
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    return signs[int(degree / 30)]

def get_house(degree, houses):
    for i in range(12):
        if i == 11:
            if degree >= houses[i] or degree < houses[0]:
                return i + 1
        elif degree >= houses[i] and degree < houses[i+1]:
            return i + 1

# dates
def get_solar_return(jd_birth, birth_date, year):
    # Get natal Sun position
    natal_sun_position = swe.calc_ut(jd_birth, swe.SUN)[0][0]

    birth_datetime = datetime.strptime(f"{birth_date}", "%Y-%m-%d")

    # Find the Solar Return
    for day in range(365):  # Check each day of the year
        jd = swe.julday(year, birth_datetime.month, birth_datetime.day + day, 0)
        sun_position = swe.calc_ut(jd, swe.SUN)[0][0]
        if sun_position >= natal_sun_position:
            # Approximate time of Solar Return
            solar_return_time = jd
            break
    return solar_return_time

def get_lunar_return(natal_info, start_date):
    natal_moon_deg = natal_info['MOON']['d']  # Access the 'd' key for degrees
    zodiac_order = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    
    # Convert natal degree to 360° format
    natal_moon_long = zodiac_order.index(natal_info['MOON']['z']) * 30 + natal_moon_deg

    # Function to find next Moon return
    def find_moon_return(start_date, natal_moon_long):
        date = datetime.strptime(start_date, "%Y-%m-%d")
        init_year = date.year
        counter = 0
        marker = 1
        dates = []
        while date.year <= init_year:
            jd = swe.julday(date.year, date.month, date.day)
            transiting_moon = swe.calc_ut(jd, swe.MOON)[0][0]
            if round(transiting_moon, 6) < round(natal_moon_long, 6) and marker == 1:
                marker = 0
            elif round(transiting_moon, 6) >= round(natal_moon_long, 6) and marker == 0: 
                marker = 1
                dates.append(date.strftime("%Y-%m-%d"))
                counter += 1
            else: 
                pass
            date += timedelta(days=1)
        return dates

    # Find next Moon return
    moon_return_date = find_moon_return(start_date, natal_moon_long)
    return moon_return_date

# house info

def astro_charts(jd_ut, latitude, longitude):
    try:
        planet_names = ["SUN", "MOON", "MERCURY", "VENUS", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE", "PLUTO"]
        additional_points = ["NORTH_NODE", "MIDHEAVEN", "PART_OF_FORTUNE"]
        zodiac_dict = {
            0: 'Aries', 1: 'Taurus', 2: 'Gemini', 3: 'Cancer', 4: 'Leo', 5: 'Virgo',
            6: 'Libra', 7: 'Scorpio', 8: 'Sagittarius', 9: 'Capricorn', 10: 'Aquarius', 11: 'Pisces'
        }
        zodiac_index = {sign: index for index, sign in zodiac_dict.items()}

        planets = {}
        for i, name in enumerate(planet_names):
            logging.debug(f"Calculating position for {name}")
            calc_result = swe.calc_ut(jd_ut, i)
            if calc_result[0] is None:
                raise ValueError(f"Failed to calculate position for {name}")
            pos = calc_result[0][0]
            planets[name] = {
                "d": round(pos % 30, 1),
                "z": zodiac_dict[int(pos / 30)]
            }
            logging.debug(f"{name} position: {planets[name]}")

        logging.debug(f"Calculating houses for jd_ut={jd_ut}, lat={latitude}, lon={longitude}")
        house_cusps, ascmc = swe.houses(jd_ut, latitude, longitude, b'P')
        logging.debug(f"Raw house_cusps: {house_cusps}")
        logging.debug(f"Raw ascmc: {ascmc}")

        if house_cusps is None or ascmc is None:
            raise ValueError("Failed to calculate houses")

        # Calculate additional points
        additional_points_data = {}
        
        north_node = swe.calc_ut(jd_ut, swe.MEAN_NODE)[0][0]
        additional_points_data["NORTH_NODE"] = {
            "d": round(north_node % 30, 1),
            "z": zodiac_dict[int(north_node / 30)]
        }
        
        # Try to calculate Juno, but don't add it to additional_points if it fails
        try:
            juno = swe.calc_ut(jd_ut, swe.JUNO)[0][0]
            additional_points_data["JUNO"] = {
                "d": round(juno % 30, 1),
                "z": zodiac_dict[int(juno / 30)]
            }
            additional_points.append("JUNO")
        except:
            logging.warning("Failed to calculate Juno position. Skipping.")
        
        midheaven = ascmc[1]
        additional_points_data["MIDHEAVEN"] = {
            "d": round(midheaven % 30, 1),
            "z": zodiac_dict[int(midheaven / 30)]
        }
        
        sun_pos = planets["SUN"]["d"] + (30 * zodiac_index[planets["SUN"]["z"]])
        moon_pos = planets["MOON"]["d"] + (30 * zodiac_index[planets["MOON"]["z"]])
        asc_pos = ascmc[0]
        part_of_fortune = (asc_pos + moon_pos - sun_pos) % 360
        additional_points_data["PART_OF_FORTUNE"] = {
            "d": round(part_of_fortune % 30, 1),
            "z": zodiac_dict[int(part_of_fortune / 30)]
        }

        # House calculation
        logging.debug("Starting house calculation:")
        house_positions = {}
        for planet, data in planets.items():
            planet_pos = data["d"] + (30 * zodiac_index[data["z"]])
            logging.debug(f"Calculating house for {planet} at position {planet_pos}")
            for i in range(12):
                if i == 11:
                    if planet_pos >= house_cusps[i] or planet_pos < house_cusps[0]:
                        house_positions[planet] = 12
                        break
                elif house_cusps[i] <= planet_pos < house_cusps[i+1]:
                    house_positions[planet] = i + 1
                    break
            logging.debug(f"{planet} assigned to house {house_positions.get(planet, 'Not assigned')}")

        logging.debug("House cusps:")
        for i, cusp in enumerate(house_cusps):
            logging.debug(f"House {i+1} cusp: {cusp}")

        chart_info = {
            planet: {
                "h": house_positions.get(planet, 0),
                "z": planets[planet]["z"],
                "d": planets[planet]["d"]
            } for planet in planet_names
        }

        asc_info = {
            "z": zodiac_dict[int(ascmc[0] / 30)],
            "d": round(ascmc[0] % 30, 1)
        }

        logging.debug(f"Final chart_info: {chart_info}")
        logging.debug(f"Final asc_info: {asc_info}")
        logging.debug(f"Final additional_points_data: {additional_points_data}")

        return chart_info, asc_info, additional_points_data

    except Exception as e:
        logging.error(f"Error in astro_charts: {str(e)}")
        raise


def format_chart_data(chart):
    return {planet: {"h": data["h"], "z": data["z"], "d": round(data["d"], 1)} 
            for planet, data in chart.items()}

# generate 1 year worth of info
def get_yearly_info(year, timezone_pytz, latitude, longitude, natal_info, birth_date, birth_time):
    y_str = str(year)
    solar_return_jd = get_solar_return(to_jd_ut(birth_date, birth_time, timezone_pytz), birth_date, year)
    solar_return, sr_asc_info, sr_additional_points = astro_charts(solar_return_jd, latitude, longitude)
    
    y_date = f"{y_str}-01-01"
    lunar_return_dates = get_lunar_return(natal_info, y_date)
    
    years_dict = {
        y_str: {
            "SR": {
                "info": "Solar Return chart",
                "chart": solar_return,
            },
            "LR": {
                "info": "Lunar Return charts",
                "returns": []
            }
        }
    }
    
    for date in lunar_return_dates:
        lunar_return, lr_asc_info, lr_additional_points = astro_charts(to_jd_ut(date, "00:00", timezone_pytz), latitude, longitude)
        years_dict[y_str]["LR"]["returns"].append({
            "date": date,
            "chart": lunar_return,

        })
    
    return years_dict

# generate 2 year worth of info
def get_biyearly_info(year, timezone_pytz, latitude, longitude, natal_info, birth_date, birth_time):
    years = [year, year + 1]
    years_dict = {}
   
    for y in years:
        y_str = str(y)
        y_date = f"{y_str}-01-01"
        
        solar_return_jd = get_solar_return(to_jd_ut(birth_date, birth_time, timezone_pytz), birth_date, y)
        solar_return, sr_asc_info, sr_additional_points = astro_charts(solar_return_jd, latitude, longitude)
        
        lunar_return_dates = get_lunar_return(natal_info, y_date)
        
        years_dict[y_str] = {
            "SR": {
                "info": "Solar Return chart",
                "chart": solar_return,
            },
            "LR": {
                "info": "Lunar Return charts",
                "returns": []
            }
        }
        
        for date in lunar_return_dates:
            lunar_return, lr_asc_info, lr_additional_points = astro_charts(to_jd_ut(date, "00:00", timezone_pytz), latitude, longitude)
            years_dict[y_str]["LR"]["returns"].append({
                "date": date,
                "chart": lunar_return,
            })
    
    logging.debug(f"Biyearly dict structure: {years_dict}")
    return years_dict