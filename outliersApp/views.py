from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view, parser_classes

from rest_framework.parsers import MultiPartParser


from outliersApp.DataAnalysis import DataAnalysis



# Create your views here.
@api_view(['POST'])
@parser_classes([MultiPartParser])
def processData(request):
    if request.method == 'POST':
            files = request.FILES.getlist('excel_files')
            if not files:
                return JsonResponse({'error': 'No files were provided.'}, status=400)
            objDataAnalysis = DataAnalysis(files=files)
            objDataAnalysis.setStructuredData()       
            #outliers = objDataAnalysis.checkOutliers()     
            #outliers = objDataAnalysis.checkOutliersIQR()    
            #outliers = objDataAnalysis.getOutliersIsolationForest()
            try:
                outliers = objDataAnalysis.checkOutliers() 
            except:
                return JsonResponse({"error":"A processing error has occurred. Please check if the uploaded file is valid."},status=400)
            return JsonResponse({"results":outliers},status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@api_view(['POST'])
@parser_classes([MultiPartParser])
def checkPatterns(request):
    if request.method == 'POST':
            files = request.FILES.getlist('excel_files')
            if not files:
                return JsonResponse({'error': 'No files were provided.'}, status=400)
            objDataAnalysis = DataAnalysis(files=files)
            objDataAnalysis.setStructuredData()       
            #outliers = objDataAnalysis.checkOutliers()     
            #outliers = objDataAnalysis.checkOutliersIQR()
            try:    
                outliers = objDataAnalysis.checkOutliersPatterns()  
            except:
                return JsonResponse({"error":"A processing error has occurred. Please check if the uploaded file is valid."},status=400)
            #outliers = objDataAnalysis.checkOutliers()
            return JsonResponse({"results":outliers},status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

""" def serializeData(df):
   
        
    rename_columns = {"Id": "RegistryId"}
        
    df.rename(columns = rename_columns, inplace=True)

    registry_resource = RegistryResource()
    # Load the pandas dataframe into a tablib dataset
    dataset = Dataset().load(df)
        
    # Call the import_data hook and pass the tablib dataset
    result = registry_resource.import_data(dataset,\
             dry_run=True, raise_errors = True)

    if not result.has_errors():
        result = registry_resource.import_data(dataset, dry_run=False)
        print(result.rows) """