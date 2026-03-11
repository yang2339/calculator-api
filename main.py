from fastapi import FastAPI, status, HTTPException, Depends
from google.cloud import bigquery

# Dependency method to provide a BigQuery client
# This will be used by the other endpoints where a database connection is necessary
def get_bq_client():
    # client automatically uses Cloud Run's service account credentials
    client = bigquery.Client()
    try:
        yield client
    finally:
        client.close()

app = FastAPI()


@app.get("/", status_code=200)
def read_root():
    """
    Health check endpoint.

    Returns:
    - JSON object indicating that the API is running successfully
    """
    return {"status": "healthy"}


@app.get("/add/{a}/{b}", status_code=200)
def add(a: str, b: str):
    """
    Add two numbers together.

    Parameters:
    - a: First number
    - b: Second number

    Returns:
    - JSON object containing the operation name, input values, and sum

    Raises:
    - 422 error if either argument is not a valid number
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Both 'a' and 'b' must be valid numbers."
        )

    return {"operation": "add", "a": a, "b": b, "result": a + b}


@app.get("/subtract/{a}/{b}", status_code=200)
def subtract(a: str, b: str):
    """
    Subtract the second number from the first number.

    Parameters:
    - a: First number
    - b: Second number

    Returns:
    - JSON object containing the operation name, input values, and difference

    Raises:
    - 422 error if either argument is not a valid number
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Both 'a' and 'b' must be valid numbers."
        )

    return {"operation": "subtract", "a": a, "b": b, "result": a - b}


@app.get("/multiply/{a}/{b}", status_code=200)
def multiply(a: str, b: str):
    """
    Multiply two numbers.

    Parameters:
    - a: First number
    - b: Second number

    Returns:
    - JSON object containing the operation name, input values, and product

    Raises:
    - 422 error if either argument is not a valid number
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Both 'a' and 'b' must be valid numbers."
        )

    return {"operation": "multiply", "a": a, "b": b, "result": a * b}


@app.get("/divide/{a}/{b}", status_code=200)
def divide(a: str, b: str):
    """
    Divide the first number by the second number.

    Parameters:
    - a: First number
    - b: Second number

    Returns:
    - JSON object containing the operation name, input values, and quotient

    Raises:
    - 422 error if either argument is not a valid number
    - 422 error if the second number is zero
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Both 'a' and 'b' must be valid numbers."
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

    Parameters:
    - a: First number
    - b: Second number
    - c: Third number

    Returns:
    - JSON object containing the operation name, input values, and average

    Raises:
    - 422 error if any argument is not a valid number
    """
    try:
        a = float(a)
        b = float(b)
        c = float(c)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="All arguments must be valid numbers."
        )

    return {"operation": "average", "a": a, "b": b, "c": c, "result": (a + b + c) / 3}


@app.get("/power/{a}/{b}", status_code=200)
def power(a: str, b: str):
    """
    Raise the first number to the power of the second number.

    Parameters:
    - a: Base number
    - b: Exponent

    Returns:
    - JSON object containing the operation name, input values, and result of exponentiation

    Raises:
    - 422 error if either argument is not a valid number
    """
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Both 'a' and 'b' must be valid numbers."
        )

    return {"operation": "power", "a": a, "b": b, "result": a ** b}


@app.get("/percentage/{part}/{whole}", status_code=200)
def percentage(part: str, whole: str):
    """
    Calculate what percentage the part is of the whole.

    Parameters:
    - part: The portion value
    - whole: The total value

    Returns:
    - JSON object containing the operation name, input values, and percentage result

    Raises:
    - 422 error if either argument is not a valid number
    - 422 error if the whole value is zero
    """
    try:
        part = float(part)
        whole = float(whole)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Both 'part' and 'whole' must be valid numbers."
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


@app.get("/dbwritetest", status_code=200)
def dbwritetest(bq: bigquery.Client = Depends(get_bq_client)):
    """
    Writes a simple test row to a BigQuery table.

    Uses the `get_bq_client` dependency method to establish a connection to BigQuery.
    """
    # Define a Python list of objects that will become rows in the database table
    # In this instance, there is only a single object in the list
    row_to_insert = [
        {
            "endpoint": "/dbwritetest",
            "result": "Success",
            "status_code": 200
        }
    ]
    
    # Use the BigQuery interface to write our data to the table
    # If there are errors, store them in a list called `errors`
    # YOU MUST UPDATE YOUR PROJECT AND DATASET NAME BELOW BEFORE THIS WILL WORK!!!
    errors = bq.insert_rows_json("sp26-mgmt54500-dev.calculator.api_logs", row_to_insert)

    # If there were any errors, raise an HTTPException to inform the user
    if errors:
        # Log the full error to your Cloud Run logs for debugging
        print(f"BigQuery Insert Errors: {errors}")
        
        # Raise an exception to the API user
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to log data to BigQuery",
                "errors": errors  # Optional: return specific BQ error details
            }
        )

    # If there were NOT any errors, send a friendly response message to the API caller
    return {"message": "Log entry created successfully"}