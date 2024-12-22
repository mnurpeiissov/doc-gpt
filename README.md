# Doc GPT 

Ask questions about your documents without ever giving away your data. 

# How it works:

1. Upload your documents
2. Ask questions like using Chat GPT

System will answer questions related to your documents and nothing else.

# How to run:

You will need docker engine and internet on your system. If you dont have docker installed please refer to https://docs.docker.com/engine/install/

Once you have docker please proceed to cloning this repository:

`git clone https://github.com/mnurpeiissov/doc-gpt.git`

After successfull cloning, please proceed to repository and start the application

`cd document-gpt`

`docker compose up`

This will start `backend`, `database` and `frontend`. After everything has started properly, you can access the application.

To access the application paste `http://localhost:3000` to your browser. Click on **Upload** -> **Choose Files** and choose your documents in .txt, .pdf, .doc formats and click **upload** button. This will trigger the process of uploading documents on the background. As of now, the progress bar does not work properly, so no need to worry, just wait for the `successfully indexed` message. Now you are good to go to talk to you documents. Navigate to the **Query** tab and ask you questions. Enjoy! 


### Backend
Backend will be available on `http://localhost:8000` and swagger on `http://localhost:8000/docs`

FastAPI was used to create endpoints for uploading and querying the documents. Project structure and some boilerplate code was inspired from Tiangolo's (Sebastian Ramirez) FastAPI full-stack application https://github.com/fastapi/full-stack-fastapi-template/tree/master




### Frontend
Frontend will be available on `http://localhost:3000`

React JS was used for developing the frontend. For now, only two endpoints are available `upload` and `query`




### Database
Postgres was chosen to store the embeddings with the help of pgvector extension. 
The table needed for storing document embeddings and metadata will be created automatically 

## Notes
Currently the application does not support Users and Authentication mechanisms. Hence, all the endpoints are available to everyone. 


## Future plans

1. Introduce users and authentication
2. Use alembic for schema creation and migration
3. Update the frontend