## Welcome to the Steve's FastAPI CRUD API! with Swagger built-in!

---

I used FastAPI and Pydantic (since it came with built-in schema verification in case I extend the framework) so that I could also leverage the swagger documentation without having to put in any extra effort.

NOTE: (Mon - 27th Oct, 2025) The latest update uses GitHub Actions to perform CI/CD operations and currently uses Docker-Compose and dockerfile to containerize and deploy application. The runner is triggered from "MY" local laptop by going to the actions folder and issuing a "./run.sh" command to start the runner and connect to GitHub.

Github actions: https://www.youtube.com/watch?v=aLHyPZO0Fy0
DockerCompose: https://www.youtube.com/watch?v=QiaphZibZsE&list=PLylTohl_B_29a3AFb719IlpqmNMrAmP77&index=532&t=66s
And if you have patience: https://www.youtube.com/watch?v=zmUAz7GDDtg&list=PLylTohl_B_29a3AFb719IlpqmNMrAmP77&index=533&t=37s

The above line was added to demo the triggering of the pipeline. Please ensure that DOCKER services are running locally for the compose to run the app and execute the tests.

---

# Instructions to work with the app:

# Use the following command to execute uvicorn locally with reload option:

# > uvicorn app:app --reload

# Use the following command to execute tests:

# > pytest test_app.py --disable-warnings -v

---

## Use - /docs to access the swagger interface when the app is running

## Available Endpoints:

1. Health Check

   GET /health

   Returns the health status of the API with timestamp.

2. Create Item

   POST /items/

   JSON Body Example:

   {
   "name": "Sample Item",
   "description": "A description",
   "price": 10.5,
   "quantity": 2
   }

3. List All Items

   GET /items/

   Returns a list of all items.

4. Get Item by ID

   GET /items/{item_id}

   Replace {item_id} with the integer ID of the item.

5. Update Item by ID

   PUT /items/{item_id}

   JSON Body Example:

   {
   "name": "Updated Item",
   "description": "Updated description",
   "price": 15.0,
   "quantity": 3
   }

6. Delete Item by ID

   DELETE /items/{item_id}

   Replace {item_id} with the integer ID of the item.

---

Note: If anyone wants to try running this locally, please use "pip install" to install the following dependencies:

fastapi

uvicorn

python-json-logger

pytest

httpx
