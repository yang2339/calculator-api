from fastapi import FastAPI, status, HTTPException
app = FastAPI()


@app.get("/", status_code=200)
def read_root():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/add/{a}/{b}", status_code=200)
def add(a: float, b: float):
    """
    Add two numbers together.
    
    Parameters:
    - a: First number
    - b: Second number
    
    Returns:
    - JSON object with the result
    """
    return {"result": a + b}


@app.get("/subtract/{a}/{b}", status_code=200)
def subtract(a: float, b: float):
    """
    Subtract the second number from the first number.

    Parameters:
    - a: First number
    - b: Second number

    Returns:
    - JSON object with the result
    """
    return {"result": a - b}


@app.get("/multiply/{a}/{b}", status_code=200)
def multiply(a: float, b: float):
    """
    Multiply two numbers.

    Parameters:
    - a: First number
    - b: Second number

    Returns:
    - JSON object with the result
    """
    return {"result": a * b}


@app.get("/divide/{a}/{b}", status_code=200)
def divide(a: float, b: float):
    """
    Divide the first number by the second number.

    Parameters:
    - a: First number
    - b: Second number

    Returns:
    - JSON object with the result

    Raises:
    - HTTP 422 error if b is zero
    """
    if b == 0:
        raise HTTPException(
            status_code=422,
            detail="Division by zero is not allowed. Please provide a non-zero value for b."
        )
    return {"result": a / b}


@app.get("/average/{a}/{b}/{c}", status_code=200)
def average(a: float, b: float, c: float):
    """
    Calculate the average of three numbers.

    Parameters:
    - a: First number
    - b: Second number
    - c: Third number

    Returns:
    - JSON object with the result
    """
    return {"result": (a + b + c) / 3}


@app.get("/power/{a}/{b}", status_code=200)
def power(a: float, b: float):
    """
    Raise the first number to the power of the second number.

    Parameters:
    - a: Base number
    - b: Exponent

    Returns:
    - JSON object with the result
    """
    return {"result": a ** b}


@app.get("/percentage/{part}/{whole}", status_code=200)
def percentage(part: float, whole: float):
    """
    Calculate what percentage the part is of the whole.

    Parameters:
    - part: The portion value
    - whole: The total value

    Returns:
    - JSON object with the result

    Raises:
    - HTTP 422 error if whole is zero
    """
    if whole == 0:
        raise HTTPException(
            status_code=422,
            detail="The whole value cannot be zero when calculating a percentage."
        )
    return {"result": (part / whole) * 100}