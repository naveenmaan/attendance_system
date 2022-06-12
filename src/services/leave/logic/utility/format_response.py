

def format_response(response, request):
    """
    method to format the response based on the request details
    Args:
        response:
        request: {
            skip: 10,
            limit: 10
        }

    Returns:

    """

    length = 1 if isinstance(response, dict) else len(response)
    has_previous_page = False
    has_next_page = False

    if isinstance(response, dict):
        length = length if response else 0

    if request.get("skip"):
        has_previous_page = True
        length = max(0, length-request['skip'])

        response = {} if isinstance(response, dict) else response[request.get("skip"):]

    if request.get("limit"):
        has_next_page = True if len(response) > request.get("limit") else False
        length = max(0, length - request['skip'])

        response = {} if isinstance(response, dict) else response[:request.get("limit")]

    return {
        "data": response,
        "total_page": length,
        "has_previous_page": has_previous_page,
        "has_next_page": has_next_page,
    }