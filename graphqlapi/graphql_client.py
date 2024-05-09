import requests
import json

class GraphQLClient:
    def __init__(self, token):
        """Initializes the GraphQL client with the provided GitHub token."""
        self.token = token
        self.url = 'https://api.github.com/graphql'

    def run_query(self, query):
        """Executes a GraphQL query against the GitHub API."""
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        request = requests.post(self.url, headers=headers, json={'query': query})

        if request.status_code == 200:
            return request.json()
        else:
            raise Exception(f"Query failed with status code {request.status_code} and message: {request.text}")

    def search_repositories(self, keyword, language='Python', stars=10000, first=5):
        """Searches repositories based on a keyword and other criteria."""
        query = f"""
        {{
          search(query: "{keyword} in:readme in:description in:name language:{language} stars:>{stars}", type: REPOSITORY, first: {first}) {{
            edges {{
              node {{
                ... on Repository {{
                  name
                  owner {{
                    login
                  }}
                  stargazers {{
                    totalCount
                  }}
                }}
              }}
            }}
          }}
        }}
        """
        return self.run_query(query)
