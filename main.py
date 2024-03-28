from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, validator, Field, ValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Jinjatemplate for index file
templates = Jinja2Templates(directory="templates")


class Package(BaseModel):
    width: float = Field(..., gt=0, description="Width of the package in centimeters")
    height: float = Field(..., gt=0, description="Height of the package in centimeters")
    length: float = Field(..., gt=0, description="Length of the package in centimeters")
    mass: float = Field(..., gt=0, description="Mass of the package in kilograms")
    volume_limit: float = Field(1000000, gt=0, description="Volume limit in cubic centimeters")
    dimension_limit: float = Field(150, gt=0, description="Dimension limit in centimeters")
    weight_limit: float = Field(20, gt=0, description="Weight limit in kilograms")

    # example validator
    # @validator("mass")
    # def validate_mass(cls, value):
    #     if value > 100:
    #         raise ValueError("Mass cannot exceed 100 kilograms")
    #     return value




def calculate_volume(width, height, length):
    return width * height * length


def sort(width: float, height: float, length: float, mass: float,
         volume_limit: float = 1000000, dimension_limit: float = 150, weight_limit: float = 20) -> str:
    """
    Sorts the package into the appropriate stack based on its dimensions and mass.
    :param width: The width of the package in centimeters.
    :param height: The height of the package in centimeters.
    :param length: The length of the package in centimeters.
    :param mass: The mass of the package in kilograms.
    :param volume_limit: The maximum allowed volume of the package in cubic centimeters.
    :param dimension_limit: The maximum allowed dimension of the package in centimeters.
    :param weight_limit: The maximum allowed weight of the package in kilograms.
    :return: The name of the stack where the package should go: STANDARD, SPECIAL, or REJECTED.
    """
    volume = calculate_volume(width, height, length)

    if any(dim <= 0 for dim in (width, height, length)) or mass < 0:
        raise ValueError("Dimensions and mass must be non-negative numbers.")

    if volume >= volume_limit or width >= dimension_limit or height >= dimension_limit or length >= dimension_limit:
        if mass >= weight_limit:
            return "REJECTED"
        else:
            return "SPECIAL"
    else:
        if mass >= weight_limit:
            return "SPECIAL"
        else:
            return "STANDARD"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/sort_package")
async def sort_package(package_data: Package):
    try:
        package = Package.validate(package_data)  # Input validations like weight limit and this can be handled in JS or API level
        result = sort(package.width, package.height, package.length, package.mass)
        return JSONResponse(content={"result": result})
    except ValidationError as e:
        error_messages = []
        for error in e.errors():
            error_messages.append(f"Error in field '{error['loc'][0]}': {error['msg']}")
        raise HTTPException(status_code=422, detail=error_messages)
    except ValueError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": str(e)})
