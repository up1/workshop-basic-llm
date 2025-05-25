import weaviate
from weaviate.classes.init import Auth

def connect_to_weaviate():
    client = weaviate.connect_to_local()
    return client

if __name__ == "__main__":
    client = connect_to_weaviate()
    print("Weaviate db is ready:", client.is_ready())
    client.close()