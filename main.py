from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, validator, Field, ValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinjatemplate for index file
templates = Jinja2Templates(directory="templates")


class Package(BaseModel):
    width: float = Field(..., gt=0, description="Width of the package in centimeters")
    height: float = Field(..., gt=0, description="Height of the package in centimeters")
    length: float = Field(..., gt=0, description="Length of the package in centimeters")
    mass: float = Field(..., gt=0, description="Mass of the package in kilograms")

    # example validator
    # @validator("mass")
    # def validate_mass(cls, value):
    #     if value > 100:
    #         raise ValueError("Mass cannot exceed 100 kilograms")
    #     return value


def calculate_volume(width, height, length):
    return width * height * length


def sort(width: float, height: float, length: float, mass: float) -> str:
    """
    Sorts the package into the appropriate stack based on its dimensions and mass.
    :param width: The width of the package in centimeters.
    :param height: The height of the package in centimeters.
    :param length: The length of the package in centimeters.
    :param mass: The mass of the package in kilograms.
    :return: The name of the stack where the package should go: STANDARD, SPECIAL, or REJECTED.
    """
    volume = calculate_volume(width, height, length)

    if any(dim <= 0 for dim in (width, height, length)) or mass < 0:
        raise ValueError("Dimensions and mass must be non-negative numbers.")

    if volume >= 1000000 or width >= 150 or height >= 150 or length >= 150:
        if mass >= 20:
            return "REJECTED"
        else:
            return "SPECIAL"
    else:
        if mass >= 20:
            return "SPECIAL"
        else:
            return "STANDARD"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/sort_package/")
async def sort_package(package_data: Package):
    try:
        package = Package.validate(
            package_data)  # Input validations like weight limit and this can be handled in JS or API level
        result = sort(package.width, package.height, package.length, package.mass)
        return JSONResponse(content={"result": result})
    except ValidationError as e:
        error_messages = []
        for error in e.errors():
            error_messages.append(f"Error in field '{error['loc'][0]}': {error['msg']}")
        raise HTTPException(status_code=422, detail=error_messages)
    except ValueError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": str(e)})
