from duckduckgo_search import AsyncDDGS
from typing import List, Dict
import requests

def test_proxy(proxy):
    try:
        response = requests.get("http://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5)
        print("Proxy is working:", response.json())
        return True
    except requests.exceptions.RequestException as e:
        print("Proxy failed:", e)
        return False




def format_search_results(results: List[Dict[str, str]]) -> str:
    formatted_results = []
    
    for result in results:
        title = result.get("title", "No title available")
        href = result.get("href", "No link available")
        body = result.get("body", "No description available")
        
        formatted_results.append(
            f"**Title:** {title}\n"
            f"**Link:** {href}\n"
            f"**Description:** {body}\n"
            "---"
        )
    
    return "\n".join(formatted_results)



async def search_handler(query: str, search_type: str):
    addgs = AsyncDDGS()
    if search_type == "text":
        results = list(await addgs.atext(query,max_results=10))
        return results
    elif search_type == "image":
        results = list(await addgs.aimages(query,max_results=5))
        return results
    elif search_type == "news":
        results = list(await addgs.anews(query,max_results=5))
        return results
    elif search_type == "maps":
        results = list(await addgs.amaps(query,max_results=5))
    elif search_type == "video":
        results = list(await addgs.avideos(query,max_results=5))
        return results
    else:
        raise ValueError("Invalid search type")
    





async def fetch_recommendtions(input):
    pass



