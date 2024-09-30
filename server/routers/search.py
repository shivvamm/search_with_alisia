import asyncio
from fastapi import APIRouter,HTTPException,Query,status
from fastapi.responses import JSONResponse
from models.schemas import Query
from typing import Optional,List
from utils.search import search_handler
from utils.chat import get_descision,chat_handler,get_search_type
router = APIRouter()


@router.post("/search",status_code=status.HTTP_200_OK)
async def search(query: Query, search_type: str):
    try:
        resources = []
        results=[]
        response=""
        if search_type == "text":
            to_sreach = await get_descision(query.query)
            
            if to_sreach:
                results = await search_handler(query.query, search_type)
                response = await chat_handler(query.query,query.session_id,results,resources="")
            else:
                response = await chat_handler(query.query,query.session_id,results="",resources="")
            return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": status.HTTP_200_OK,
                "data": response,
                "resources": resources,
                "message": "Search completed successfully."
            }
        )
        
        elif search_type == "other":
            print(query.search_type_resources)
            valid_search_types = ["Image", "News", "Maps","Video"]
            requested_search_type = query.search_type_resources
            if not all(item in valid_search_types for item in requested_search_type):
                return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Invalid search type provided."}
                )     
            results=await search_handler(query.query, "text")
            if len(query.search_type_resources) > 0:
                resources = await asyncio.gather(*(search_handler(query.query, i.lower()) for i in requested_search_type))
                # for i in query.search_type_resources:
                    # resources.append(search_handler(query.query, i.lower()))
                    


            response = await chat_handler(query.query,query.session_id,results,resources)
            return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": status.HTTP_200_OK,
                "data": response,
                "resources": resources,
                "message": "Search completed successfully."
            }
            )
    except HTTPException as http_exc:
        raise http_exc
    
    except ValueError as val_exc:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(val_exc)}
        )
    
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "An unexpected error occurred. Please try again later."}
        )
    

@router.get("/autocomplete")
async def recommmendation(input:str):
    try:
        # response = await auto_recommendation(query.query, search_type)
        return {"response": "fr"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/searchnew",status_code=status.HTTP_200_OK)
async def search(query: Query, search_type: str):
    try:
        resources = []
        results=[]
        response=""
        search_type = await get_search_type(query.query)
        print(search_type)
        if "Text" in search_type:
            to_sreach = await get_descision(query.query)
            
            if to_sreach:
                results = await search_handler(query.query, search_type)
                response = await chat_handler(query.query,query.session_id,results,resources="")
            else:
                response = await chat_handler(query.query,query.session_id,results="",resources="")
            return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": status.HTTP_200_OK,
                "data": response,
                "resources": resources,
                "message": "Search completed successfully."
            }
        )
        
        # elif search_type == "other":
        #     print(query.search_type_resources)
        #     valid_search_types = ["Image", "News", "Maps","Video"]
        #     requested_search_type = query.search_type_resources
        #     if not all(item in valid_search_types for item in requested_search_type):
        #         return JSONResponse(
        #         status_code=400,
        #         content={"status": "error", "message": "Invalid search type provided."}
        #         )     
        #     results=await search_handler(query.query, "text")
        #     if len(query.search_type_resources) > 0:
        #         resources = await asyncio.gather(*(search_handler(query.query, i.lower()) for i in requested_search_type))
        #         # for i in query.search_type_resources:
        #             # resources.append(search_handler(query.query, i.lower()))
                    


        #     response = await chat_handler(query.query,query.session_id,results,resources)
        return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": status.HTTP_200_OK,
            "data": "Hello",
            "resources": resources,
            "message": "Search completed successfully."
        }
        )
    except HTTPException as http_exc:
        raise http_exc
    
    except ValueError as val_exc:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(val_exc)}
        )
    
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "An unexpected error occurred. Please try again later."}
        )