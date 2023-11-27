import pandas as pd
from sklearn.ensemble import IsolationForest

class DataAnalysis:
    def __init__(self,files) -> None:
        self.files=files
        self.dataFrame=None
    def setStructuredData(self):
        index = 0
        for file in self.files:
                try:
                    df = pd.read_excel(file)
                    df = df.dropna()
                    df['File']=file.name
                    if(index==0):
                         result_df=df
                         index=index+1
                    else:
                        # Concatenar los dos DataFrames verticalmente (axis=0)
                        result_df = pd.concat([result_df, df], axis=0, ignore_index=True)
                    # Realizar operaciones con el DataFrame

                except pd.errors.EmptyDataError:
                    print(f"Warning: Empty DataFrame for file {file.name}")
        self.dataFrame =  result_df
        #print(result_df.info())

    def checkOutliersContextLogic(self):
        outlier_speed_df = self.getOutliersSpeedPaceDistance()
        outlier_speed_df =  outlier_speed_df.sort_values('UserId')
        outliers_groupby_userid = outlier_speed_df.groupby('UserId')
        
        count_groupby =  outliers_groupby_userid.sum()
        
        finalOutliers=[]
        # Iterar sobre las filas
        for index, row in count_groupby.iterrows():
            #print("index",index)
            outlier_rows_runner = outlier_speed_df[outlier_speed_df['UserId'] == index]
            average_values_runner,std_values_runner = self.getAvgsAndStdRunner(index)
            #print("avg runner",average_values_runner)
            for index2, row2 in outlier_rows_runner.iterrows():
                if((row2['AverageSpeedInMetersPerSecond']>average_values_runner['AverageSpeedInMetersPerSecond'] - 2 * std_values_runner['AverageSpeedInMetersPerSecond']) and 
                   (row2['AverageHeartRateInBeatsPerMinute']>average_values_runner['AverageHeartRateInBeatsPerMinute'] - 2 * std_values_runner['AverageHeartRateInBeatsPerMinute']) and 
                   (row2['TotalElevationGainInMeters']<average_values_runner['TotalElevationGainInMeters'] + 2* std_values_runner['TotalElevationGainInMeters']) and
                   (row2['DistanceInMeters']<average_values_runner['DistanceInMeters'] + 2* std_values_runner['DistanceInMeters']) and
                   (row2['DurationInSeconds']<average_values_runner['DurationInSeconds'] + 2* std_values_runner['DurationInSeconds']) and
                   (row2['AveragePaceInMinutesPerKilometer']<average_values_runner['AveragePaceInMinutesPerKilometer']+ 2*std_values_runner['AveragePaceInMinutesPerKilometer'])):
                        continue
                else:
                    outliner_dict = row2.to_dict() 
                    outliner_dict['Average'] = average_values_runner.to_dict()
                    finalOutliers.append(outliner_dict)
        return finalOutliers
    
    def isCheater(self,row2,idUser):
        average_values_runner,std_values_runner = self.getAvgsAndStdRunner(idUser)
        if((row2['AverageSpeedInMetersPerSecond']>average_values_runner['AverageSpeedInMetersPerSecond'] ) and 
                   (row2['AverageHeartRateInBeatsPerMinute']>average_values_runner['AverageHeartRateInBeatsPerMinute'] ) and 
                   (row2['DistanceInMeters']<average_values_runner['DistanceInMeters'] ) and
                   (row2['DurationInSeconds']<average_values_runner['DurationInSeconds'] ) and
                   (row2['AveragePaceInMinutesPerKilometer']<average_values_runner['AveragePaceInMinutesPerKilometer'])):
                        return False
        else:
            if((row2['AverageSpeedInMetersPerSecond']<average_values_runner['AverageSpeedInMetersPerSecond'] ) and 
                   (row2['DistanceInMeters']>average_values_runner['DistanceInMeters'] ) and
                   (row2['DurationInSeconds']>average_values_runner['DurationInSeconds'] ) and 
                   (row2['Steps']>average_values_runner['Steps'] ) ):
                    return False
            else:
                 return True
    
    def checkOutliers(self):
        outlier_df = self.getOutliersSpeedPaceDistance()
        #outlier_isolation_forest_df = self.getOutliersIsolationForest()

        finalOutliersSpeed = self.checkOutliersIQR(outliers=outlier_df)
        #finalOutliersIsolationForest = self.checkOutliersIQR(outliers=outlier_isolation_forest_df)
        #finalOutliers = {}
        #finalOutliers["finalOutliersSpeed"] = finalOutliersSpeed
        print(len(finalOutliersSpeed))
        #finalOutliers["finalOutliersIsolationForest"] = finalOutliersIsolationForest

        return finalOutliersSpeed
    
    def checkOutliersPatterns(self):
        outlier_isolation_forest_df = self.getOutliersIsolationForest()

        finalOutliersIsolationForest = self.checkOutliersIQR(outliers=outlier_isolation_forest_df)
        print(len(finalOutliersIsolationForest))
        return finalOutliersIsolationForest

    def checkOutliersIQR(self,outliers):
        #outlier_speed_df = self.getOutliersSpeed()
        #outlier_speed_df = self.getOutliersIsolationForest()
        outliers =  outliers.sort_values('UserId')
        outliers_groupby_userid = outliers.groupby('UserId')
        
        count_groupby =  outliers_groupby_userid.sum()
        
        finalOutliers=[]
        # Iterar sobre las filas
        for idUser, row in count_groupby.iterrows():
            outlier_rows_runner = outliers[outliers['UserId'] == idUser]
            limit_values_runner = self.getOutliersIQR(idUser)     
            for index2, row2 in outlier_rows_runner.iterrows():
                metricsList = []
                if((row2['AverageSpeedInMetersPerSecond']<limit_values_runner['AverageSpeedInMetersPerSecond']['lowerLimit']) | (row2['AverageSpeedInMetersPerSecond']>limit_values_runner['AverageSpeedInMetersPerSecond']['upperLimit'])):
                    metricsList.append('AverageSpeedInMetersPerSecond')
                if((row2['DurationInSeconds']<limit_values_runner['DurationInSeconds']['lowerLimit']) | (row2['DurationInSeconds']>limit_values_runner['DurationInSeconds']['upperLimit'])):
                    metricsList.append('DurationInSeconds')
                if((row2['DistanceInMeters']<limit_values_runner['DistanceInMeters']['lowerLimit']) | (row2['DistanceInMeters']>limit_values_runner['DistanceInMeters']['upperLimit'])):
                    metricsList.append('DistanceInMeters')
                if((row2['Steps']<limit_values_runner['Steps']['lowerLimit']) | (row2['Steps']>limit_values_runner['Steps']['upperLimit'])):
                    metricsList.append('Steps')
                if((row2['AveragePaceInMinutesPerKilometer']<limit_values_runner['AveragePaceInMinutesPerKilometer']['lowerLimit']) | (row2['AveragePaceInMinutesPerKilometer']>limit_values_runner['AveragePaceInMinutesPerKilometer']['upperLimit'])):
                    metricsList.append('AveragePaceInMinutesPerKilometer')
                if((row2['TotalElevationGainInMeters']<limit_values_runner['TotalElevationGainInMeters']['lowerLimit']) | (row2['TotalElevationGainInMeters']>limit_values_runner['TotalElevationGainInMeters']['upperLimit'])):
                    metricsList.append('TotalElevationGainInMeters')
                if((row2['AverageHeartRateInBeatsPerMinute']<limit_values_runner['AverageHeartRateInBeatsPerMinute']['lowerLimit']) | (row2['AverageHeartRateInBeatsPerMinute']>limit_values_runner['AverageHeartRateInBeatsPerMinute']['upperLimit'])):
                    metricsList.append('AverageHeartRateInBeatsPerMinute')
                if(len(metricsList)>0):
                    if(self.isCheater(row2=row2,idUser=idUser)):                         
                        outliner_dict = row2.to_dict() 
                        outliner_dict['Reason'] = metricsList
                        average_values_runner,std_values_runner = self.getAvgsAndStdRunner(idUser)
                        outliner_dict['Average'] = average_values_runner.to_dict()
                        finalOutliers.append(outliner_dict)
        return finalOutliers      


    
    def getAvgsAndStdRunner(self,UserId):
        rows_runner = self.dataFrame[self.dataFrame['UserId'] == UserId]
        columns_of_interest = ['UserId','DurationInSeconds', 'DistanceInMeters', 'Steps', 'AverageSpeedInMetersPerSecond', 'AveragePaceInMinutesPerKilometer', 'TotalElevationGainInMeters','AverageHeartRateInBeatsPerMinute']
        rows_runner= rows_runner[columns_of_interest]
        avgs = rows_runner.mean()
        stds = rows_runner.std()            
        return avgs,stds
    
    def getOutliersIQR(self,UserId):
        rows_runner = self.dataFrame[self.dataFrame['UserId'] == UserId]
        columns_of_interest = ['UserId','DurationInSeconds', 'DistanceInMeters', 'Steps', 'AverageSpeedInMetersPerSecond', 'AveragePaceInMinutesPerKilometer', 'TotalElevationGainInMeters','AverageHeartRateInBeatsPerMinute']
        rows_runner= rows_runner[columns_of_interest]
        metrics={}
        for column in columns_of_interest:
            # Calcular el IQR para la columna 
            q1 = rows_runner[column].quantile(0.25)
            q3 = rows_runner[column].quantile(0.75)
            iqr = q3 - q1
            lowerLimit = q1 -1.5*iqr
            upperLimit = q3 +1.5*iqr
           
            metrics[column]={
                "lowerLimit":lowerLimit,
                "upperLimit":upperLimit
                }
            
        return metrics

    def getOutliersSpeedPaceDistance(self):
        outlier_speed = 7
        outlier_pace = 2.381
        outlier_distance = 42000
        return self.dataFrame[(self.dataFrame['AverageSpeedInMetersPerSecond'] > outlier_speed) | (self.dataFrame['AveragePaceInMinutesPerKilometer'] < outlier_pace) | ( self.dataFrame['DistanceInMeters'] > outlier_distance)]

    def getOutliersDistance(self):
        outlier_distance = 42000
        return self.dataFrame[self.dataFrame['DistanceInMeters'] > outlier_distance]

    def getOutliersIsolationForest(self):
        # Inicializa el modelo Isolation Forest
        model = IsolationForest(contamination=0.05, random_state=42)  # Ajusta el parámetro de contaminación según tus necesidades
        columns_of_interest = ['UserId','DurationInSeconds', 'DistanceInMeters', 'Steps', 'AverageSpeedInMetersPerSecond', 'AveragePaceInMinutesPerKilometer', 'TotalElevationGainInMeters','AverageHeartRateInBeatsPerMinute']
        data = self.dataFrame[columns_of_interest]
        copyDf = self.dataFrame
        # Entrena el modelo
        model.fit(data)

        # Predice las anomalías
        copyDf['anomalias'] = model.predict(data)

        # Filtra los registros anómalos
        anomalous_records = copyDf[copyDf['anomalias'] == -1]
        return anomalous_records

    