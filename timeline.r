twt <- read_csv("tweets_01-08-2021 copy.csv")
# creating new column of just date from date column
twt$date2 <- as.Date(twt$date)

# creating subset data based on pre-elec (2016 only), elec-period, elec-day, and post-elec
# ucsb president data timeline referenced
Trump.primary.2016 <- subset(twt, date2 > as.Date("2015-06-14") & date2 < as.Date("2016-07-19"))
Trump.elec.2016 <- subset(twt, date2 > as.Date("2016-07-18") & date2 < as.Date("2016-11-08"))
Trump.elecday.2016 <- subset(twt, date2 > as.Date("2016-11-07") & date2 < as.Date("2016-11-09"))
Trump.post.2016 <- subset(twt, date2 > as.Date("2016-11-08") & date2 < as.Date("2017-01-21"))
Trump.elec.2020 <- subset(twt, date2 > as.Date("2020-08-23") & date2 < as.Date("2020-11-03"))
Trump.elecday.2020 <- subset(twt, date2 > as.Date("2020-11-02") & date2 < as.Date("2020-11-04"))
Trump.post.2020 <- subset(twt, date2 > as.Date("2020-11-03"))
