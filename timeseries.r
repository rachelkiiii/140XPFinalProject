# Taig's Time Series
```{r creating data objects}
library(readr)
library(dplyr)

# read in data
trump_tweets <- read_csv("clean_tweets.csv")
clean_tweets <- trump_tweets[,c(5,7)]

# organize by date
ordered_tweets <- clean_tweets %>% arrange(date)

# sentiment analysis on whole dataset (will take a few minutes)
text <- ordered_tweets$cleaned_text
nrc_T <- get_nrc_sentiment(text)

# create trust data frame
trust_column <- nrc_T[,"trust",drop=F]
date_column <- ordered_tweets[,"date", drop=F]
trust_ts_df <- cbind(date_column,trust_column)

# create date and time vectors for time series
trust <- nrc_T[,"trust"]
date <- ordered_tweets[,"date", drop=T]
```


```{r creating time series}
library(tseries)
library(forecast)

# create trust time series object
trust_ts <- irts(date,trust)

# plot (it looks terrible, I know) - note that the all points are at discrete values
plot(trust_ts)
points(trust_ts, col="red")
```

```{r changing discrete trust score to weekly average score}
# Convert the date column to actual Date type
trust_ts_df$date <- as.Date(trust_ts_df$date)
head(trust_ts_df)

# Calculate the monthly average trust score
trust_monthly_avg_df <- trust_ts_df %>%
  mutate(month = lubridate::month(date),
         year = lubridate::year(date)) %>%
  mutate(year_month = lubridate::make_date(year, month)) %>%
  group_by(year_month) %>%
  summarize(trust_monthly_avg = mean(trust, na.rm=T))
head(trust_monthly_avg_df)

# Create a monthly trust_ts object
trust_monthly_ts <- ts(trust_monthly_avg_df$trust_monthly_avg, start = c(2009,05), frequency = 12)
tsdisplay(trust_monthly_ts)
auto.arima(trust_monthly_ts)
```
