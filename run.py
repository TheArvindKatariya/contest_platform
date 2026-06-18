#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
