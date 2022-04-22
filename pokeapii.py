import requests

def get_pokemon_info(name):
    """
    Gets all information about a specified Pokemon retrieved from the PokeAPI
    :param name: Pokemon name
    :returns: Dictionary of Pokemon info, if successful. None, if not.
    """
    print("Getting Pokemon info...", end='')

    if name is None:
        print('error: missing name paramater')
        return
    
    name = name.strip().lower()
    if name == '':
        print('error: empty')
        return
    url = "https://pokeapi.co/api/v2/pokemon/" + name
    resp_msg = requests.get(url)
    if resp_msg.status_code == 200:
        print('success')
        return resp_msg.json()
    else:
        print('failed. Code:', resp_msg.status_code)
        return

def get_pokemon_image_url(name):
    pokemon_dict = get_pokemon_info(name)
    if pokemon_dict:
        return pokemon_dict['sprites']['other']['official-artwork']['front_default']




def get_pokemon_list(limit=100, offset=0):
    url = 'https://pokeapi.co/api/v2/pokemon'
    
    params = {
        'limit': limit,
        'offset': offset
    }

    resp_msg = requests.get(url, params=params)

    if resp_msg.status_code == 200:

        dict = resp_msg.json()
        return [p['name'] for p in dict['results']]
    else:
        print('failed to get pokemn list')
        print('response code:', resp_msg.status_code)
        print(resp_msg.text)