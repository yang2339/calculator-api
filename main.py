from fastapi import FastAPI, status, HTTPException

app = FastAPI()


@app.get("/", status_code=200)
def read_root():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/add/{a}/{b}", status_code=200)
def add(a: str, b: str):
    """
    Add two numbers together.
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Both 'a' and 'b' must be valid numbers"
        )

    return {"operation": "add", "a": a, "b": b, "result": a + b}


@app.get("/subtract/{a}/{b}", status_code=200)
def subtract(a: str, b: str):
    """
    Subtract the second number from the first number.
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Both 'a' and 'b' must be valid numbers"
        )

    return {"operation": "subtract", "a": a, "b": b, "result": a - b}


@app.get("/multiply/{a}/{b}", status_code=200)
def multiply(a: str, b: str):
    """
    Multiply two numbers.
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Both 'a' and 'b' must be valid numbers"
        )

    return {"operation": "multiply", "a": a, "b": b, "result": a * b}


@app.get("/divide/{a}/{b}", status_code=200)
def divide(a: str, b: str):
    """
    Divide the first number by the second number.
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Both 'a' and 'b' must be valid numbers"
        )

    if b == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Division by zero is not allowed. Please provide a non-zero value for b."
        )

    return {"operation": "divide", "a": a, "b": b, "result": a / b}


@app.get("/average/{a}/{b}/{c}", status_code=200)
def average(a: str, b: str, c: str):
    """
    Calculate the average of three numbers.
    """
    try:
        a = float(a)
        b = float(b)
        c = float(c)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="All arguments must be valid numbers"
        )

    return {"operation": "average", "a": a, "b": b, "c": c, "result": (a + b + c) / 3}


@app.get("/power/{a}/{b}", status_code=200)
def power(a: str, b: str):
    """
    Raise the first number to the power of the second number.
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Both 'a' and 'b' must be valid numbers"
        )

    return {"operation": "power", "a": a, "b": b, "result": a ** b}


@app.get("/percentage/{part}/{whole}", status_code=200)
def percentage(part: str, whole: str):
    """
    Calculate what percentage the part is of the whole.
    """
    try:
        part = float(part)
        whole = float(whole)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Both 'part' and 'whole' must be valid numbers"
        )

    if whole == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The whole value cannot be zero when calculating a percentage."
        )

    return {
        "operation": "percentage",
        "part": part,
        "whole": whole,
        "result": (part / whole) * 100
    }