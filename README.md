# Methods of Advanced Data Engineering (module at FAU) Project

The structure of this project for my open data project in the MADE module at FAU was forked from the provided [project template](https://github.com/jvalue/made-template).
This repository contains (a) an individual data science project that was developed over the course of the semester, and (b) the exercises that were submitted over the course of the semester.

## Project Work - Analyzing the impact of air pollution on cancer in the U.S.

The project work is located in the `project` folder. The question this project aimed to answer was: "How does air pollution, measured by the AQI, in the five most populous states in the U.S. correlate with the incidence of cancer?"

Air pollution is an important problem, because it affects countries all over the world and impacts many people. This project analyzed wether there is a correlation between air pollution and cancer in the five most populous states in the U.S. The air pollution is measured with the AQI (Air Quality Index) and the cancer incidence is measured with the crude rate (per 100,000 people). This project analyzed the data from the years 2006 to 2021. The data was cleaned, transformed (averaged, etc.), visualized and analyzed to find correlations.

The results are presented in two reports, one for the used and transformed data sources - the [data report](./project/data-report.pdf) - and one for the analysis, visualization and interpretation - the [analysis report](./project/analysis-report.pdf).

Two main scripts were used to analyze the data: one for downloading and transforming the data ([the data pipeline](./project/pipeline.py)), and one for [analyzing and visualizing](./project/analyze_data.py) the data. The transformed data is saved into a [database file](./data/). There are also some [tests](./project/tests.py) provided to test the data pipline. Tests and the data pipeline can be run with a bash script ([pipeline.sh](./project/pipeline.sh), [tests.sh](./project/tests.sh)). Before starting, please install the [requirements](./project/requirements.txt) with `pip install -r requirements.txt`.

The data pipeline is tested automatically with a GitHub action every time a change is made in the `project` folder and pushed to the local changes to the repository on GitHub. To see the test results, navigate to Actions → Execute Project Tests in this repository.

## Exercises

The exercises were completed using [Jayvee](https://github.com/jvalue/jayvee). For details and deadlines also see the [course schedule](https://made.uni1.de/).

### Exercise Feedback

Automated exercise feedback was provided using a GitHub action (that is defined in `.github/workflows/exercise-feedback.yml`).

To view the exercise feedback, navigate to Actions → Exercise Feedback in this repository.

The exercise feedback is executed whenever a change is made in files in the `exercise` folder and pushed to the local changes to the repository on GitHub. To see the feedback, open the latest GitHub Action run, open the `exercise-feedback` job and `Exercise Feedback` step. You should see command line output that contains output like this:

```sh
Found exercises/exercise1.jv, executing model...
Found output file airports.sqlite, grading...
Grading Exercise 1
	Overall points 17 of 17
	---
	By category:
		Shape: 4 of 4
		Types: 13 of 13
```
