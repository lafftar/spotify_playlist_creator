from spotify_api_interface import spotify_obj


def search(input_text):
    output = []
    if '/album/' or '/playlist/' in input_text:
        input_text = input_text.split('/')[-1]
    results = spotify_obj().search(input_text, type=["album", "playlist"])
    if results['albums']['total'] == 0:
        return None
    results = results["albums"]["items"]
    for result in results:
        artist_name = result["artists"][0]["name"]
        rsrc_name = result["name"]
        rsrc_url = result["external_urls"]["spotify"]
        img_url = result["images"][1]["url"]
        output.append({
            "Artist Name": artist_name,
            "Resource Name": rsrc_name,
            "Resource Url": rsrc_url,
            "Image Url": img_url
        })
    return output


# print(spotify_obj().search("rap caviar", type=["album", "playlist"])['albums']['total'])
