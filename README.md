<img
  src="shoes.jpeg"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; max-width: 200px">


# Git Shoes!


## Project Description
This is a Natural Language Processing project that undertakes the task of predicting the main coding language of repositories using their README.md files. In particular, we have chosen to go through 100+ repositories that are related to shoes and are the most starred. It is being conducted at Codeup, Data Science programme, Noether cohort, March 2023.


## Project Goals
- Determine the programming language of a given Github repository. 
- The repository must contain the word 'shoes'.


## Initial Thoughts
Intial thoughs : Java could be the most common language, followed by Python. As for the predictory words, we thought that shoe company brands or shoe types would be amongst the most common words.


## The Plan
1. Acquire data.
2. Initial exploration.
3. Clean data.
4. Create questions.
5. Split data.
6. Explore data on train set.
7. Model using Classification methods.


## Data Dictionary
| Feature | Definition |
| :-- | :-- |
| repo | repository of README.md file |
| readme_contents | text content of README.md file |
| clean | readme_content column cleaned by: <br> - lowercase all words,<br> - unicode "NKFD",<br> - encode "ASCII", <br> - decode "UTF-8" |
| stemmed | all text from the "clean" column stemmed | 
| lemmatized |  all text from the "clean" column lemmatized |


## Acquire
- Data acquired from Github.
  - Query for 'shoes' in search bar. Filter by 'Most Stars'.
- 198 README.md files acquired.
- Each row represents a repository.
- Columns represent the repository, language and README.md contents.


## Prepare
- Dropped nulls. 
  - 13 values dropped.
- Cleaned text contents:
  - lowercased
  - unicode "NKFD"
  - encode "ASCII", decode "UTF-8".
- Create stemmed and lemmatized columns.
- Split into train, validate and test sets (56/24/20).


## Explore
- Search for and establish most common words using NLP techniques.
- Look at TF-IDF scores.
- Create bigrams. (This led to the discovery of two separate film scripts in two separate README.md files.)
- Create bar plots and word clouds to visualize trends.


## Conclusion
In this project, we examined the programming languages of Github repositories based on words mentioned in README.md files that included the word 'shoes'.
By acquiring using web scraping techniques, exploring the data and creating classification models, using the decision tree, we established a model to  accurately predict the programming language 43 pc of the time. 
  - Baseline: 25% 
  - Final Model: 43%
  - Performance Increase: 73%


## Recommendations
- We recommend that those interested in shoe marketing use the results of this project to bolster or enhance the jargon they use. 


## Next Steps
- Explore bigrams and trigrams.
- Visualize the bigrams and trigrams via word clouds.


## Steps To Reproduce
1. Clone this Repository.
2. Use functions in acquire.py file.
3. Use functions in prepare.py to clean and prep data.
4. Use same configurations for models.
