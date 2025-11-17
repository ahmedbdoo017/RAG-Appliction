from enum import Enum 

class ResponseEnums (Enum):
        
    FILE_TYPE_NOT_SUPPORTED = "file type not supported"
    FILE_UPLOAD_FAILED = "file upload failed" 
    FILE_SIZE_EXCEEDED = "file size exceeded"
    FILE_UPLOAD_SUCSESS = "file upload sucsses"

    PROCESSING_SUCESS = "processing_sucesss"
    PROCESSING_FAILD = "processing faild"
