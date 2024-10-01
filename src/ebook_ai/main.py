from module import Module

module = Module()
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(module.app, host="0.0.0.0", port=8000)