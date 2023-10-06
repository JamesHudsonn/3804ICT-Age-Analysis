# Install and load necessary libraries

install.packages("caret")

install.packages("rpart")

install.packages("rpart.plot")

library(caret)
library(rpart)
library(rpart.plot)

set.seed(123) # for reproducibility


data <- read.csv("C:/Users/James/3804ICT/Assignment/Age-Analysis/3804ICT-Age-Analysis/preprocessed_age_copy.csv")
data <- data[data$Gender %in% c("male", "female"), ]

# Splitting data into training and testing sets (70-30 split as an example)
trainIndex <- createDataPartition(data$Manner_of_death, p = 0.7, list = FALSE)

trainData <- data[trainIndex,]
testData <- data[-trainIndex,]



tree <- rpart(Gender ~ Birth_year + Age_of_death, data = trainData)
#tree <- rpart(Age_of_death ~ Occupation + Birth_year + Manner_of_death + Associated_Countries + Associate_Country_Life_Expectancy, data = trainData)
#rpart.plot(tree, space=4, split.cex = 1.5, nn.border.col=0)


# Predict using the decision tree
predictedValues <- predict(tree, testData, type = "class")

# Calculate the accuracy
accuracy <- sum(predictedValues == testData$Manner_of_death) / nrow(testData)
print(paste("Accuracy:", round(accuracy*100, 2), "%"))


confusionMatrix(predictedValues, testData$Age_of_death)






