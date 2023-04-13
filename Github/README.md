# Who are the top contributors of a Repo? 
Leveraging GitHub API 




- [Generate a personal access token on github.](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)  
Settings > Developer settings > Personal access tokens > Generate new token  

- Calls a repository's endpoint (Apache Hadoop Github Repo's contributors’). 

- Extracts the JSON corresponding to the first 100 contributors from the API. 

Parses the information and stores as a SQL database.

