<img
  src="shoes.jpeg"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; max-width: 300px">


# Git Shoes!


## Project Description
This repository contains functions and workbooks for a group project to predict the programming language of Github repositories using Natural Language Processing techniques. It is being conducted at Codeup, Data Science programme, Noether cohort, March 2023.


## Initial Thoughts
Intial thoughs is that Java will be the most common language, followed by python. As for the predictory words, shoe company brands or shoe types will be the most common words.

## The Plan
1. Acquire data
2. Initial exploration.
3. Clean data.
4. Create questions.
5. Split data.
6. Explore data on train set.
7. Model using Classification.


## Data Dictionary
| Feature | Definition |
| :-- | :-- |
| repo | repository of readme file |
| readme_contents | text content of readme file |
| clean | readme_content column cleaned by: <br> - lowercase all words,<br> - unicode "NKFD",<br> - encode "ASCII", <br> - decode "UTF-8" |
| stemmed | all text from the "clean" column stemmed | 
| lemmatized |  all text from the "clean" column lemmatized |


## Acquire
- Data acquired from Github.
  - Query for 'shoes' in search bar. Filter by 'Most Stars'.
- 198 Readme files acquired.
- Each row represents a repository.
- Columns represent the repository, language, and readme contents.


## Prepare
- Dropped nulls. 
  - 13 values dropped.
- Cleaned text contents:
  - lowercased
  - unicode "NKFD"
  - encode "ASCII", decode "UTF-8"
- Create stemmed and lemmatized columns.
- Split into train, validate, and test sets (56/24/20).


## Explore
- Search for most common words.
- Create bar plots and word clouds to visualize trends.

## Conclusion


## Next Steps
- Explore bigrams and trigrams.
- Visualize them via word clouds.


## Steps to Reproduce
1. Clone this Repo.
2. Use functions in acquire.py file.
3. Use functions in prepare.py to clean and prep data.
4. Use same configurations for models.



