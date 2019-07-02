
library(dplyr)
library(ggmap)
library(stringr)
library(tidytext)
library(leaflet)
library(ggplot2)
library(wordcloud)

## Load Data
tweet_data <- read.csv(file="data/Tweets.csv")


## Show tweet table
head(tweet_data, n = 100)

tweet_data %>% 
    group_by(airline,airline_sentiment) %>% 
    summarise(n()) %>%
    as.data.frame()

tweet_ratings <- tweet_data %>% 
    group_by(airline,airline_sentiment) 

## Plot positive vs negative tweets by airline

s <- ggplot(tweet_ratings, aes(airline, fill = airline_sentiment)) + geom_bar(position = "fill")

cbPalette <- c("#ef8a62", "#f7f7f7", "#67a9cf")
s + scale_fill_manual(values=cbPalette)

## Plot number of tweets by location

load("dataviz/top_locations.rda")

as.data.frame(table(tweet_data['tweet_location'])) %>% 
  arrange(desc(Freq)) %>% 
  filter(Freq > 50) %>% 
  slice(2:100)

leaflet(
  top_locs_with_name %>% 
  slice(2:100) %>%
  group_by(long = lon,lat) %>% 
  summarise(count = sum(n))
  ) %>% 
  addTiles() %>% 
  addCircleMarkers(
    radius = ~count/40,
    stroke = FALSE, 
    fillOpacity = 0.5
  )


## Tokenize the words into a corpus
data(stop_words)

airlines = tibble(text = c("united","usairways","americanair","southwestair","jetblue","virginamerica"))

text_df <- tibble(line = 1:length(as.character(tweet_data$text)), text = as.character(tweet_data$text))

text_df <- text_df %>%  
  mutate(text = str_replace_all(text, "https://t.co/[A-Za-z\\d]+|http://[A-Za-z\\d]+|&amp;|&lt;|&gt;|RT|https", "")) %>%
  unnest_tokens(word, text) #, token = "regex", pattern = reg_words)

text_df <- text_df %>% anti_join(stop_words)
text_df <- text_df %>% anti_join(airlines,by = c("word" = "text"))

## Plot word count frequency

text_df %>%
  count(word, sort = TRUE) %>%
  as.data.frame()

text_df %>%
  filter(word != "flight") %>%
  count(word, sort = TRUE) %>%
  filter(n > 400) %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(word, n)) +
  geom_col() +
  xlab(NULL) +
  coord_flip()

## Plot word cloud - Just for Michael

text_df %>% 
  filter(word != "flight") %>%
  count(word) %>%
  with(wordcloud(word, n, scale=c(4,0.5),max.words = 50))






