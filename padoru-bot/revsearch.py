import requests
from config import SAUCENAO_TOKEN


def return_sauce_dic(similarity, thumbnail, url, title, mem_id, name):
    return {
        "found": True,
        "similarity": similarity,
        "thumbnail": thumbnail,
        "url": url,
        "title": title,
        "id": mem_id,
        "name": name
    }


def get_sauce_nao(url):
    # From the APIDocs, important params
    output_type = "2"
    api_key = SAUCENAO_TOKEN
    testmode = "1"
    db = "999"
    numres = "16"
    # You may be wondering about my stylish line breaks,
    # I don't like it when pep8 complains
    sauce_nao_api = (f"https://saucenao.com/search.php?"
                     f"output_type={output_type}"
                     f"&api_key={api_key}"
                     f"&testmode={testmode}"
                     f"&db={db}"
                     f"&numres={numres}"
                     f"&url={url}")
    sauce_dic = requests.get(sauce_nao_api).json()
    sauce_res = sauce_dic["results"]
    index = 0
    while index < len(sauce_res):
        cur_pos = sauce_res[index]
        cur_head = cur_pos["header"]
        cur_data = cur_pos["data"]
        cur_url = cur_data["ext_urls"]
        if float(cur_head["similarity"]) > 50:
            if "pixiv_id" in cur_data:
                return return_sauce_dic(cur_head["similarity"],
                                        cur_head["thumbnail"],
                                        cur_url[0],
                                        cur_data["title"],
                                        cur_data["pixiv_id"],
                                        cur_data["member_name"])
            elif "seiga_id" in cur_data:
                return return_sauce_dic(cur_head["similarity"],
                                        cur_head["thumbnail"],
                                        cur_url[0],
                                        cur_data["title"],
                                        cur_data["seiga_id"],
                                        cur_data["member_name"])
            break
        else:
            return {"found": False}
        index += 1
