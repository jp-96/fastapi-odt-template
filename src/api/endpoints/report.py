from fastapi import UploadFile, File, APIRouter
import os

router = APIRouter()

folder_path = "/opt/report-engine/code/data/reports/"

# Lists all templates
@router.get("/",summary="Lists all templates.", tags=["Report"])
def ListTemplates():
    result = []

    for file_name in [f for f in os.listdir(folder_path)]:
        file_path = folder_path + file_name
        res = dict()
        file_stat = os.stat(file_path)
        if os.path.splitext(file_name)[1] == ".odt":
            res["name"] = file_name
            res["size"] = file_stat.st_size
            result.append(res)

    return result

# Get single template
@router.get("/{name}",summary="Get single template.", tags=["Report"])
def GetTemplate(name: str):
    file_path = folder_path + name
    file_stats = os.stat(file_path)
    res = dict()
    res["name"] = name
    res["size"] = file_stats.st_size
    
    return res

# Delete template
@router.delete("/{name}",summary="Deletes a template.", tags=["Report"])
def DeleteTemplate(name: str):
    file_path = folder_path + name
    os.remove(file_path)
    return "Item deleted successfully."

# Upload new template
@router.post("/", summary="Uploads new template.", tags=["Report"])
def SaveTemplate(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        name = file.filename.replace(" ", "_")
        name = file.filename.replace("-", "_")
       
        with open(name, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
        os.rename(name, folder_path + name)
    
    return {"message": f"Successfully uploaded {name}"}
