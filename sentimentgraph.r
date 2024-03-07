# Load the ggplot2 package
library(ggplot2)
processed <- read.csv("~/Downloads/twt.csv")

# Convert sentiment values to numeric
processed$sentiment <- as.numeric(gsub("[^0-9.-]", "", processed$sentiment))

processed$time_block <- factor(processed$time_block, levels = c("Trump_primary_2016", "Trump_elec_2016", "Trump_elecday_2016", "Trump_post_2016", "Trump_elec_2020", "Trump_elecday_2020", "Trump_post_2020"))

# Create a table of sentiment counts for each time block
sentiment_counts <- table(processed$time_block, processed$sentiment_class)

# Print the table
print(sentiment_counts)

barplot(sentiment_counts[, -5], beside = TRUE, col = c("red", "green", "blue", "orange", "pink", "skyblue", "yellow"),
        legend.text = TRUE, args.legend = list(x = "topright"),
        main = "Sentiment Counts for Each Time Block", ylab = "Count",
        xlab = "Time Block")

total <- rowSums(sentiment_counts[, -1])
sentiment_counts_percent <- sentiment_counts[, -1] / total * 100
sentiment_counts_percent
