from fastapi import FastAPI, HTTPException
import httpx

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

    #if user exists
    submissions = user_data.get("submitStats",{}).get("acSubmissionNum",[])  

    total_solved = submissions[0].get("count") if len(submissions)>0 else 0

    return{
        "platform":"LeetCode",
        "username":username,
        "total_solved":total_solved
    }      

    
