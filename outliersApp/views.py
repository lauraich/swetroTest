from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from outliersApp.DataAnalysis import DataAnalysis


# Process Data API Endpoint
@api_view(["POST"])
@parser_classes([MultiPartParser])
def processData(request):
    """
    API endpoint for processing data and detecting outliers.

    Method: POST

    Parameters:
    - 'excel_files': List of Excel files to be processed.

    Returns:
    - JSON response containing the results of outlier detection.

    Possible Errors:
    - 400 Bad Request: If no files are provided or if a processing error occurs.
    """
    if request.method == "POST":
        files = request.FILES.getlist("excel_files")
        if not files:
            return JsonResponse({"error": "No files were provided."}, status=400)
        objDataAnalysis = DataAnalysis(files=files)
        objDataAnalysis.setStructuredData()
        try:
            outliers = objDataAnalysis.checkOutliers()
        except:
            return JsonResponse(
                {
                    "error": "A processing error has occurred. Please check if the uploaded file is valid."
                },
                status=400,
            )
        return JsonResponse({"results": outliers}, status=200)
    return JsonResponse({"error": "Invalid request method."}, status=400)


# Check Patterns API Endpoint
@api_view(["POST"])
@parser_classes([MultiPartParser])
def checkPatterns(request):
    """
    API endpoint for checking patterns in the provided data.

    Method: POST

    Parameters:
    - 'excel_files': List of Excel files to be analyzed for patterns.

    Returns:
    - JSON response containing the results of pattern analysis.

    Possible Errors:
    - 400 Bad Request: If no files are provided or if a processing error occurs.
    """
    if request.method == "POST":
        files = request.FILES.getlist("excel_files")
        if not files:
            return JsonResponse({"error": "No files were provided."}, status=400)
        objDataAnalysis = DataAnalysis(files=files)
        objDataAnalysis.setStructuredData()
        try:
            outliers = objDataAnalysis.checkOutliersPatterns()
        except:
            return JsonResponse(
                {
                    "error": "A processing error has occurred. Please check if the uploaded file is valid."
                },
                status=400,
            )
        return JsonResponse({"results": outliers}, status=200)
    return JsonResponse({"error": "Invalid request method."}, status=400)
