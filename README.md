# receipt-processor
The Receipt Processor is a Flask-based API that processes receipt data and awards points based on specific rules. Users can submit receipt details to the API, which calculates and returns a unique ID for each receipt. With this ID, users can retrieve the points awarded to each receipt. This project is Dockerized to ensure easy setup and deployment.

### Requirements 
Docker -  The application is containerized using Docker.

### Setup and installations 
1. Clone the repository
   
    ````python
   git clone https://github.com/priyankabgda111/receipt-processor.git
   cd receipt-processor
     ````
3. Build the Docker Image
    ````python
   docker build -t receipt-processor .
     ````
4. Run the Docker Container
   ````python
   docker run -p 5000:5000 receipt-processor
     ````



