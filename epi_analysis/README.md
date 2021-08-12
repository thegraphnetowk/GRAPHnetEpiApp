# EpiGraphHub Shiny App
![architecture](architecture.png)

This application provides an interactive analytical COVID-19 dashboard for the African continent.

## Deploying the App
The application can be run locally or from Docker containers.
before Building the container make sure an `.env_db` file exists with the proper variables declared.

to start the containers, you need to have docker and docker-compose installed. Make sure you have the 
following directories in the root of your clone of this repository: `cleanCSV`(containins linelist CSVs)
`maps` (containing the mapps in Geopackage format to be loaded), and `dicts` (containing the name dictionaries
as JSON files). Then run the following command:

```bash
docker-compose build
```  

after the containers are built they can be started with

```bash
docker-compose -p epigraph -f docker-compose.yml --env-file .env_db up --build
```
One the containers are up the database will be accessible from on the host on por 5432 and can be accessed with any postgresql client.
To stop the containers you can use the following command:

```bash
docker-compose -p epigraph -f docker-compose.yml --env-file .env_db down
```

While the containers are up, you can also access the Shinyapp running in the container,
by pointing your browser to [http://localhost:3838](http://localhost:3838).
## Running the shinyapp from the terminal
For development purposes it may be convenient to simply run the app outside the container for testing.

In this case, use this command, from the root of the repository:
```
R -e "require(shiny); runApp('shinyapp', host='0.0.0.0', port=3838)"
``` 

### Upgrading Base images
From time-to-time it is useful to update the containers with the latest versions of base images (PosgreSQL, pgadmin4, etc). This can be achieved with the following command:

```bash
docker-compose down && docker-compose build --pull && docker-compose up -d
``` 

## Running shinyapp with Rstudio

### Step 0
If you're working on the code and need to get the app up and down easily for feedback you can still use Rstudio to launch it locally.
If you have only worked with Renku in our project you will neet to download R & Rstudio first avilable at :

https://cran.r-project.org/mirrors.html

https://rstudio.com/products/rstudio/

### Step 1
Once Rstudio is setup you can select the cloned repo GRAPHnetEpiApp and launch the project.

### Step 2

Open in the editor either ui.R / server.R or global.R and in the editor's toolbar you will find the "Run App" button, click it and _voilà_

In your console, you will have a line notifying you on which adress you can open the app in your navigator. Copy the link in your adress bar and _voilà_




## To Know more
### Working with containers
* [Getting started with Docker](https://docs.docker.com/get-started/overview/)
* [Overview of Docker Compose](https://docs.docker.com/compose/)
* [Docker desktop ( for Mac and Windows users)](https://docs.docker.com/desktop/)
* [Using Docker as Shiny server](https://github.com/rocker-org/shiny)
