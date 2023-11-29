import pandas as pd
from sklearn.ensemble import IsolationForest


class DataAnalysis:
    def __init__(self, files) -> None:
        """
        Constructor for the DataAnalysis class.

        Parameters:
        - files: List of File objects to be processed.
        """
        self.files = files
        self.dataFrame = None

    def setStructuredData(self):
        """
        Reads and structures the data from Excel files into a pandas DataFrame.

        Notes:
        - Drops NaN values.
        - Adds a 'File' column to identify the source file.
        """
        index = 0
        for file in self.files:
            try:
                df = pd.read_excel(file)
                df = df.dropna()
                df["File"] = file.name
                if index == 0:
                    result_df = df
                    index = index + 1
                else:
                    # Concatenate the two DataFrames vertically (axis=0)
                    result_df = pd.concat([result_df, df], axis=0, ignore_index=True)
            except pd.errors.EmptyDataError:
                print(f"Warning: Empty DataFrame for file {file.name}")
        self.dataFrame = result_df

    def isCheater(self, row2, idUser):
        """
        Checks if a specific record indicates a potential cheater based on predefined conditions.

        Parameters:
        - row2: DataFrame row representing a specific record.
        - idUser: Identifier for the user.

        Returns:
        - Boolean indicating whether the record suggests cheating.
        """
        average_values_runner, std_values_runner = self.getAvgsAndStdRunner(idUser)
        if (
            (
                row2["AverageSpeedInMetersPerSecond"]
                > average_values_runner["AverageSpeedInMetersPerSecond"]
            )
            and (
                row2["AverageHeartRateInBeatsPerMinute"]
                > average_values_runner["AverageHeartRateInBeatsPerMinute"]
            )
            and (row2["DistanceInMeters"] < average_values_runner["DistanceInMeters"])
            and (row2["DurationInSeconds"] < average_values_runner["DurationInSeconds"])
            and (
                row2["AveragePaceInMinutesPerKilometer"]
                < average_values_runner["AveragePaceInMinutesPerKilometer"]
            )
        ):
            return False
        else:
            if (
                (
                    row2["AverageSpeedInMetersPerSecond"]
                    < average_values_runner["AverageSpeedInMetersPerSecond"]
                )
                and (
                    row2["DistanceInMeters"] > average_values_runner["DistanceInMeters"]
                )
                and (
                    row2["DurationInSeconds"]
                    > average_values_runner["DurationInSeconds"]
                )
                and (row2["Steps"] > average_values_runner["Steps"])
            ):
                return False
            else:
                return True

    def checkOutliers(self):
        """
        Checks for outliers in the data using IQR (Interquartile Range) method.
        Based on atypical data found on speed, pace, and distance compared to the average person.
        Returns:
        - List of dictionaries containing information about outliers.
        """
        outlier_df = self.getOutliersSpeedPaceDistance()

        finalOutliersSpeed = self.checkOutliersIQR(outliers=outlier_df)

        return finalOutliersSpeed

    def checkOutliersPatterns(self):
        """
        Checks for outliers in the data using Isolation Forest method.

        Returns:
        - List of dictionaries containing information about outliers.
        """
        outlier_isolation_forest_df = self.getOutliersIsolationForest()

        finalOutliersIsolationForest = self.checkOutliersIQR(
            outliers=outlier_isolation_forest_df
        )
        print(len(finalOutliersIsolationForest))
        return finalOutliersIsolationForest

    def checkOutliersIQR(self, outliers):
        """
        Checks for outliers in the data using IQR (Interquartile Range) method.

        Parameters:
        - outliers: DataFrame containing potential outliers.

        Returns:
        - List of dictionaries containing information about outliers.
        """
        outliers = outliers.sort_values("UserId")
        outliers_groupby_userid = outliers.groupby("UserId")

        count_groupby = outliers_groupby_userid.sum()

        finalOutliers = []
        # Iterate over rows
        for idUser, row in count_groupby.iterrows():
            outlier_rows_runner = outliers[outliers["UserId"] == idUser]
            limit_values_runner = self.getOutliersIQR(idUser)
            for index2, row2 in outlier_rows_runner.iterrows():
                metricsList = []
                if (
                    row2["AverageSpeedInMetersPerSecond"]
                    < limit_values_runner["AverageSpeedInMetersPerSecond"]["lowerLimit"]
                ) | (
                    row2["AverageSpeedInMetersPerSecond"]
                    > limit_values_runner["AverageSpeedInMetersPerSecond"]["upperLimit"]
                ):
                    metricsList.append("AverageSpeedInMetersPerSecond")
                if (
                    row2["DurationInSeconds"]
                    < limit_values_runner["DurationInSeconds"]["lowerLimit"]
                ) | (
                    row2["DurationInSeconds"]
                    > limit_values_runner["DurationInSeconds"]["upperLimit"]
                ):
                    metricsList.append("DurationInSeconds")
                if (
                    row2["DistanceInMeters"]
                    < limit_values_runner["DistanceInMeters"]["lowerLimit"]
                ) | (
                    row2["DistanceInMeters"]
                    > limit_values_runner["DistanceInMeters"]["upperLimit"]
                ):
                    metricsList.append("DistanceInMeters")
                if (row2["Steps"] < limit_values_runner["Steps"]["lowerLimit"]) | (
                    row2["Steps"] > limit_values_runner["Steps"]["upperLimit"]
                ):
                    metricsList.append("Steps")
                if (
                    row2["AveragePaceInMinutesPerKilometer"]
                    < limit_values_runner["AveragePaceInMinutesPerKilometer"][
                        "lowerLimit"
                    ]
                ) | (
                    row2["AveragePaceInMinutesPerKilometer"]
                    > limit_values_runner["AveragePaceInMinutesPerKilometer"][
                        "upperLimit"
                    ]
                ):
                    metricsList.append("AveragePaceInMinutesPerKilometer")
                if (
                    row2["TotalElevationGainInMeters"]
                    < limit_values_runner["TotalElevationGainInMeters"]["lowerLimit"]
                ) | (
                    row2["TotalElevationGainInMeters"]
                    > limit_values_runner["TotalElevationGainInMeters"]["upperLimit"]
                ):
                    metricsList.append("TotalElevationGainInMeters")
                if (
                    row2["AverageHeartRateInBeatsPerMinute"]
                    < limit_values_runner["AverageHeartRateInBeatsPerMinute"][
                        "lowerLimit"
                    ]
                ) | (
                    row2["AverageHeartRateInBeatsPerMinute"]
                    > limit_values_runner["AverageHeartRateInBeatsPerMinute"][
                        "upperLimit"
                    ]
                ):
                    metricsList.append("AverageHeartRateInBeatsPerMinute")
                if len(metricsList) > 0:
                    if self.isCheater(row2=row2, idUser=idUser):
                        outliner_dict = row2.to_dict()
                        outliner_dict["Reason"] = metricsList
                        (
                            average_values_runner,
                            std_values_runner,
                        ) = self.getAvgsAndStdRunner(idUser)
                        outliner_dict["Average"] = average_values_runner.to_dict()
                        finalOutliers.append(outliner_dict)
        return finalOutliers

    def getAvgsAndStdRunner(self, UserId):
        """
        Calculates average and standard deviation values for a specific runner.

        Parameters:
        - UserId: Identifier for the user.

        Returns:
        - Tuple containing average and standard deviation DataFrames.
        """
        rows_runner = self.dataFrame[self.dataFrame["UserId"] == UserId]
        columns_of_interest = [
            "UserId",
            "DurationInSeconds",
            "DistanceInMeters",
            "Steps",
            "AverageSpeedInMetersPerSecond",
            "AveragePaceInMinutesPerKilometer",
            "TotalElevationGainInMeters",
            "AverageHeartRateInBeatsPerMinute",
        ]
        rows_runner = rows_runner[columns_of_interest]
        avgs = rows_runner.mean()
        stds = rows_runner.std()
        return avgs, stds

    def getOutliersIQR(self, UserId):
        """
        Calculates outlier limits for a specific runner using IQR (Interquartile Range) method.

        Parameters:
        - UserId: Identifier for the user.

        Returns:
        - Dictionary containing outlier limits for different metrics.
        """
        rows_runner = self.dataFrame[self.dataFrame["UserId"] == UserId]
        columns_of_interest = [
            "UserId",
            "DurationInSeconds",
            "DistanceInMeters",
            "Steps",
            "AverageSpeedInMetersPerSecond",
            "AveragePaceInMinutesPerKilometer",
            "TotalElevationGainInMeters",
            "AverageHeartRateInBeatsPerMinute",
        ]
        rows_runner = rows_runner[columns_of_interest]
        metrics = {}
        for column in columns_of_interest:
            # Calculate the IQR for the column
            q1 = rows_runner[column].quantile(0.25)
            q3 = rows_runner[column].quantile(0.75)
            iqr = q3 - q1
            lowerLimit = q1 - 1.5 * iqr
            upperLimit = q3 + 1.5 * iqr

            metrics[column] = {"lowerLimit": lowerLimit, "upperLimit": upperLimit}

        return metrics

    def getOutliersSpeedPaceDistance(self):
        """
        Retrieves records that are potential outliers based on speed, pace, and distance.

        Returns:
        - DataFrame containing potential outliers.
        """
        outlier_speed = 7
        outlier_pace = 2.381
        outlier_distance = 42000
        return self.dataFrame[
            (self.dataFrame["AverageSpeedInMetersPerSecond"] > outlier_speed)
            | (self.dataFrame["AveragePaceInMinutesPerKilometer"] < outlier_pace)
            | (self.dataFrame["DistanceInMeters"] > outlier_distance)
        ]

    """  def getOutliersDistance(self):
        outlier_distance = 42000
        return self.dataFrame[self.dataFrame["DistanceInMeters"] > outlier_distance] 
    """

    def getOutliersIsolationForest(self):
        """
        Retrieves records that are potential outliers using the Isolation Forest method.

        Returns:
        - DataFrame containing potential outliers.
        """
        model = IsolationForest(contamination=0.05, random_state=42)
        columns_of_interest = [
            "UserId",
            "DurationInSeconds",
            "DistanceInMeters",
            "Steps",
            "AverageSpeedInMetersPerSecond",
            "AveragePaceInMinutesPerKilometer",
            "TotalElevationGainInMeters",
            "AverageHeartRateInBeatsPerMinute",
        ]
        data = self.dataFrame[columns_of_interest]
        copyDf = self.dataFrame

        model.fit(data)

        copyDf["anomalias"] = model.predict(data)

        anomalous_records = copyDf[copyDf["anomalias"] == -1]
        return anomalous_records
