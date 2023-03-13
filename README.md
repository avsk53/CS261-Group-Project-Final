# CS261-Group-Project-Final

## Running the system
To run the system, you will need to run the backend and frontend servers at the same time, then visit `localhost:3000/` in your browser.
## Running the backend
To run the backend of the system, navigate to the Backend directory and run (on Mac/Linux):
```
sudo docker-compose up --build
```
On Windows, you can instead use Docker Desktop to compose the `docker-compose.yml` file.

## Running the frontend
To run the frontend of the system, you will first need to install Node version `v16.16.0`. After this, navigate to the Frontend directory and run:
```
npm install
```
After the dependencies are installed, run:
```
npm run dev
```