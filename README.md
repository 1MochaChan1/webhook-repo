# Dev Assessment - Webhook Receiver

Please use this repository for constructing the Flask webhook receiver.

*******************

## Setup

* Create a new virtual environment

```bash
pip install virtualenv
```

* Create the virtual env

```bash
virtualenv venv
```

* Activate the virtual env

```bash
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate     # On Windows
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Run the flask application (In production, please use Gunicorn)

```bash
python run.py
```

* The endpoint is at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

You need to use this as the base and setup the flask app. Integrate this with MongoDB (commented at `app/extensions.py`)

*******************

## MongoDB Setup

* Create a file:  
  `app/local.env`

* Add your MongoDB connection string:

```env
MONGO_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/<db>?retryWrites=true&w=majority
```

* In your code, load it with:

```python
from dotenv import load_dotenv
load_dotenv("app/local.env")
```

* Use the URI from the environment:

```python
import os
uri = os.getenv("MONGO_URI")
```

* Pass this `uri` to your MongoDB client setup in `extensions.py`.

*******************

## Local Testing with ngrok

To expose your local server for testing (e.g., GitHub webhooks):

```bash
ngrok http 5000
```

Use the generated public URL (e.g. `https://<random>.ngrok.io`) as your webhook endpoint.
