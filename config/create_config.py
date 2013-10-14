from config import Config

if __name__ == "__main__":
    json = Config().to_json()
    print json
