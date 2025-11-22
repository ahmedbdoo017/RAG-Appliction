from enum import Enum 

class ResponseEnums (Enum):
        
    FILE_TYPE_NOT_SUPPORTED = "file type not supported"
    FILE_UPLOAD_FAILED = "file upload failed" 
    FILE_SIZE_EXCEEDED = "file size exceeded"
    FILE_UPLOAD_SUCSESS = "file upload sucsses"

    PROCESSING_SUCESS = "processing_sucesss"
    PROCESSING_FAILD = "processing faild"

    NO_FILES_ERROR = "not found files"
    FILE_ID_ERROR = "no file found with this id"

    PROJECT_NOT_FOUND_ERROR = "project_not_found"
    INSERT_INTO_VECTORDB_EROOR ="insert_into_vectordb_error"
    INSERT_INTO_VECTORDB_SUCCESS ="insert_into_vectordb_success"