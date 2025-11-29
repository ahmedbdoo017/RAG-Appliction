from fastapi import FastAPI , APIRouter ,Depends , UploadFile , status , Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings , Settings
from controllers import DataController, ProjectController, ProcessController
from models import ResponseEnums,AssetTypeEnum
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.db_schemes import DataChunk , Assets
from models.ChunkModel import ChunkModel
from models.AssetModel import AssetModel
import os
import aiofiles
import logging

logger =logging.getLogger("uvicorn.error")
#create route object to use it in another files
data_router = APIRouter(
    prefix='/api/v1/data'
)

############################################ Upload File EndPoint ######################################################
@data_router.post("/upload/{project_id}")
async def upload_data (request : Request, project_id : str , file : UploadFile ,
                       app_settings : Settings = Depends(get_settings)) :
    
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    
    project = await project_model.get_project_or_create_one(project_id=project_id)


    is_valid ,result  = DataController().validate_uploaded_file(file)
    if not is_valid :
        return JSONResponse(
                        status_code = status.HTTP_400_BAD_REQUEST ,
                        content = {
                            "signal" : result
                            }
                        )
    
    file_path ,file_id  = DataController().generate_unique_filepath(orig_file_name=file.filename , project_id= project_id)
   
    try:
        # save file as chunckes at hard rather than download full file in temp memory (RAM)
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE) :
                await f.write(chunk) 

    except Exception as e :
        # save error in logger to handel clinet problem 
        logger.error(f"Error while uploading file: {e}")

        # show faild message only for user but the error message appear in log file for admin
        return JSONResponse(
                        status_code = status.HTTP_400_BAD_REQUEST ,
                        content = {
                            "signal" : ResponseEnums.FILE_UPLOAD_FAILED.value,
                            }
                        )

    # store the assets into the database
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
    asset_resoures = Assets(
        assets_project_id= project.id,
        assets_type= AssetTypeEnum.FILE.value ,
        assets_name=file_id ,
        assets_size= os.path.getsize(file_path)
    )

    asset_record = await asset_model.create_asset(asset=asset_resoures)

    return JSONResponse(
        content= {
            "signal" : ResponseEnums.FILE_UPLOAD_SUCSESS.value ,
            "file_id" : str(asset_record.id),
             
        }
    )


############################################ Process File EndPoint ######################################################
@data_router.post("/process/{project_id}")
async def process_endpoint (request : Request, project_id : str, process_request : ProcessRequest) :
    
    chunk_size = process_request.chunk_size
    overlap_size =process_request.overlap_size
    do_reset = process_request.do_reset
    
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    
    project = await project_model.get_project_or_create_one(project_id=project_id)
    
    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
                                                   
    if do_reset ==1:
        _ = await chunk_model.delete_chunks_by_project_id(project_id=project.id)

    project_files_ids = {}
    
    if process_request.file_id :
        # if user determine what file want to chunk then make chunk for this file only
        asset_record =await asset_model.get_aseet_record(
            asset_project_id=project.id,
            aseet_name= process_request.file_id
            )
        
        if asset_record is None:
            return JSONResponse(
                        status_code = status.HTTP_400_BAD_REQUEST ,
                        content = {
                            "signal" : ResponseEnums.FILE_ID_ERROR.value,
                            }
                        )

        project_files_ids ={
            asset_record.id : asset_record.assets_name
        }


    else:
        # if user didn't determine file_id to chunk so make chunking for all files in the project "i"
        project_files = await asset_model.get_all_project_aseets(
            asset_project_id=project.id,
            aseet_type =AssetTypeEnum.FILE.value
        )

        project_files_ids = {
            record.id : record.assets_name
            for record in project_files 
        }
    
    if len(project_files_ids) ==0:
         return JSONResponse(
                        status_code = status.HTTP_400_BAD_REQUEST ,
                        content = {
                            "signal" : ResponseEnums.NO_FILES_ERROR.value,
                            }
                        )




    process_controller = ProcessController(project_id=project_id)

    no_record =0
    no_files =0

    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)
    if do_reset ==1:
        _ = await chunk_model.delete_chunks_by_project_id(project_id=project.id)

    for asset_id, file_id in project_files_ids.items():

        file_content = process_controller.get_file_content(file_id=file_id)

        if file_content is None:
            logger.error(f"error while processing file_id ({file_id}) is not found ")
            continue

        file_chunks = process_controller.process_file_content(
                                                            file_id=file_id, 
                                                            file_content=file_content,
                                                            chunk_size=chunk_size,
                                                            overlap_size=overlap_size
                                                            )
        
        if file_chunks is None or len(file_chunks)==0:
            return JSONResponse(
                    status_code = status.HTTP_400_BAD_REQUEST ,
                    content = {
                        "signal" : ResponseEnums.PROCESSING_FAILD.value
                    }
            )



        file_chunks_records = [
            DataChunk(
                chunk_txt= chunk.page_content,
                chunk_metadata = chunk.metadata,
                chunk_order= i+1,
                chunk_project_id= project.id,
                chunk_asset_id= asset_id
            )
            for i, chunk in enumerate(file_chunks)
        ] 

        
        no_record += await chunk_model.insert_many_chunks(chunks=file_chunks_records)
        no_files +=1
    return JSONResponse(
        content={
            "signal": ResponseEnums.PROCESSING_SUCESS.value,
            "inserted_chunks": no_record,
            "processed_files": no_files
        }
    )