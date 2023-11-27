from rest_framework import serializers
import pandas as pd


class ExcelFileSerializer(serializers.Serializer):
    excel_file = serializers.FileField()

    def to_representation(self, instance):
        # Convertir el contenido del archivo Excel a un DataFrame de pandas
        df = pd.read_excel(instance, header=1)
        return {'data': df.to_dict()}