import googleapiclient.discovery

from google import genai
import requests
import json
import config_loader


def sum_calories(food_list: list) -> int:
    """Returns the sum of all calories in the food_list"""

    total_calories = 0.0
    
    for item in food_list:
        try:
            total_calories += item['calories']
        except KeyError:
            print(f"Error: Item {item['food_name']} is missing the 'calories' key.")
        except TypeError:
            print(f"Error: Calorie value for {item['food_name']} is not a number.")
            
    return round(total_calories,2)


def filter_food_list(nutrition_data: dict) -> list:
    """Returns a list of foods with filtered key value pairs."""

    return [
        {
            "food_name": n['food_name'],
            "calories": n['nf_calories'],
            "serving_qty": n['serving_qty'],
            "serving_unit": n['serving_unit']
        }
        for n in nutrition_data['foods']
    ]


def fetch_nutrition(ingredients: str) -> int:
    """ Passes a list of comma separated ingredients with their quantity to the nutritionix api and returns the sum of all calories in the food list """
    
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"

    headers = {
        "Content-Type": "application/json",
        "x-app-id": config_loader.NUTRITIONIX_ID,   
        "x-app-key": config_loader.NUTRITIONIX_API_KEY 
    }

    payload = {
        "query": ingredients
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    nutrition_data = response.json()

    filtered_food_list = filter_food_list(nutrition_data)
    return sum_calories(filtered_food_list)   
    

def extract_ingredients(ingredients: str) -> str:
    """Gives a list of ingredients to Gemini for sanitising and returns the sanitised response"""
    
    prompt = f"Extract the english part of the ingredients and their amount. Bring the quantity before the ingredient. Correct the tbs to tbsp. I want the ingredients to be seperated by ' and '. Ignore any food that doesn't have quantity. An example of this is; '2 tbsp cooking oil and 1 tbsp Ginger garlic paste'  \n ------ {ingredients} \n ------"
    
    client = genai.Client(api_key=config_loader.GEMINI_API_KEY)
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
    )
    return response.text


def parse_response(response: dict) -> dict | None:
    """Parses the response from the youtube api and returns a dictionary containing ingredients and title from the description of the video"""

    if response['items'][0]['snippet']['channelTitle'] == 'Food Fusion':
        description = response['items'][0]['snippet']['description']

        start = description.find('Ingredients')
        end = description.find('Directions', start)
        return {"ingredients":description[start:end], "title": response['items'][0]['snippet']['title']}
    else: 
        return None

    
def get_video_response(api_service_name: str, api_version: str) -> dict | None:
    """Prompts the user to provide the id for a food fusion video, sends it to youtube api v3 and returns a parsed response""" 

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=config_loader.YOUTUBE_API_KEY)
    print('This application finds out the total calories in a dish from the youtube channel Food Fusion (@FoodfusionPk).')
    print("You need to enter the id of the chosen video which can be found on the address bar v='{\id\}' example id: d4oqFQqFUfs")
    
    while True:
        try:
            id = input("Please enter id of the food fusion video: ")
            request = youtube.videos().list(
                part="snippet",
                id=id
            )
            
            response = request.execute()
            parsed_response = parse_response(response)
        
            if parsed_response:
                break
            else:
                print('Id does not belong to food fusion')
        except Exception as e:
            print(e) 
    
    return parsed_response



def main():
    # d4oqFQqFUfs 
    ingredients = get_video_response("youtube", "v3")
    title = ingredients['title']
    # print('youtube ingredients ',ingredients)

    sanitised_ingredients = extract_ingredients(ingredients["ingredients"])
    # print('gemini ingredients: ', sanitised_ingredients)

    total_calories = fetch_nutrition(sanitised_ingredients)
    print(f"Total calories in the {title} is", total_calories)
    

if __name__ == "__main__":
    main()