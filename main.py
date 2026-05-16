from fastapi import FastAPI, HTTPException
import httpx
from bs4 import BeautifulSoup #for web scrapping

# Initialize the FastAPI app
app = FastAPI(
    title="DevBoard API",
    description="Backend API for aggregating developer profiles",
    version="1.0.0"
)

# Define your first endpoint
@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Welcome to the DevBoard API! Let's build something awesome."
    }

#github endpoint
@app.get("/api/github/{username}")
async def get_github_stats(username:str):
    url = f"https://api.github.com/users/{username}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404,detail="User not found on Github")

    data = response.json()

    return {
        "platform": "GitHub",
        "username":data.get("login"),
        "public_repos":data.get("public_repos"),
        "followers":data.get("followers"),
        "profile_url":data.get("html_url")
     }


#leetcode endpoint
@app.get("/api/leetcode/{username}")
async def get_leetcode_stats(username:str):
    url="https://leetcode.com/graphql"
    graphql_query = """
    query ($username:String!){
        matchedUser(username: $username){
            profile {
                ranking
            }
            submitStats{
                acSubmissionNum{
                    difficulty
                    count
                }
            }
        }
    }
    """
    payload = {
        "query":graphql_query,
        "variables":{"username":username}
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url,json=payload)
        
    if response.status_code !=200:
        raise HTTPException(status_code=500,detail="Leetcode server error")

    data=response.json()
    user_data = data.get("data", {}).get("matchedUser")

    if not user_data:
        raise HTTPException(status_code=404, detail="LeetCode user not found")

    # Grab the ranking from the new profile section
    ranking = user_data.get("profile", {}).get("ranking", 0)

    submissions = user_data.get("submitStats",{}).get("acSubmissionNum",[])

    # Grab the Easy, Medium, and Hard counts from the array
    # Index 0 is All, 1 is Easy, 2 is Medium, 3 is Hard
    total_solved = submissions[0].get("count") if len(submissions) > 0 else 0
    easy_solved = submissions[1].get("count") if len(submissions) > 1 else 0
    medium_solved = submissions[2].get("count") if len(submissions) > 2 else 0
    hard_solved = submissions[3].get("count") if len(submissions) > 3 else 0 # for the safety net as new user with zero will have empty [] return by the leetcode api

    return {
        "platform": "LeetCode",
        "username": username,
        "ranking": ranking,
        "total_solved": total_solved,
        "easy_solved": easy_solved,
        "medium_solved": medium_solved,
        "hard_solved": hard_solved
    } 

#codechef endpoint
@app.get("/api/codechef/{username}")
async def get_codechef_stats(username:str):
    url = f"https://www.codechef.com/users/{username}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code !=200:
        raise HTTPException(status_code=404, detail="CodeChef User not found")

    soup = BeautifulSoup(response.text,"html.parser")

    rating_div = soup.find("div", class_="rating-number")

    if not rating_div:
        current_rating = "Unrated"

    current_rating = rating_div.text.strip()

    return {
        "platform": "CodeChef",
        "username":username,
        "current_rating":current_rating
    }




    
