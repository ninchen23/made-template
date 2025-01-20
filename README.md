# Methods of Advanced Data Engineering Project

The structure of this project for my open data project in the MADE (Methods of Advanced Data Engineering) module at FAU was forked from the provided [project template](https://github.com/jvalue/made-template).

This repository contains (a) an individual data science project that was developed over the course of the semester, and (b) the exercises that were submitted over the course of the semester.

## Project Work - Analyzing the impact of air pollution on cancer in the U.S.

The project work is located in the `project` folder. The question this project aimed to answer was: "How does air pollution, measured by the AQI, in the five most populous states in the U.S. correlate with the incidence of cancer?"

Air pollution is an important problem, because it affects countries all over the world and impacts many people. This project analyzed wether there is a correlation between air pollution and cancer in the five most populous states in the U.S. The air pollution is measured with the AQI (Air Quality Index) and the cancer incidence is measured with the crude rate (per 100,000 people). This project analyzed the data from the years 2006 to 2021. The data was cleaned, transformed (averaged, etc.), visualized and analyzed to find correlations.

The results are presented in two reports, one for the used and transformed data sources - the [data report](./project/data-report.pdf) - and one for the analysis, visualization and interpretation - the [analysis report](./project/analysis-report.pdf).

Two main scripts were used to analyze the data: one for downloading and transforming the data ([the data pipeline](./project/pipeline.py)), and one for [analyzing and visualizing](./project/analyze_data.py) the data. The transformed data is saved into a [database file](./data/). There are also some [tests](./project/tests.py) provided to test the data pipline. Tests and the data pipeline can be run with a bash script ([pipeline.sh](./project/pipeline.sh), [tests.sh](./project/tests.sh)). Before starting, please install the [requirements](./project/requirements.txt) with `pip install -r requirements.txt`.

The data pipeline is tested automatically with a GitHub action every time a change is made in the `project` folder and pushed to main branch of the repository on GitHub. To see the test results, navigate to Actions → Execute Project Tests in this repository.

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

# License Information

This repository is available under the MIT License. For more information, see the [LICENSE](./LICENSE) file. If you use this repository or parts of it and adapt e.g. the data pipeline to your need, please check the licenses of the data sources used in this project. Some information about the data sources can be found in the [data report](./project/data-report.pdf).

If you use something from this repository, please reference it. Thank you!

## Reports License

The reports provided in this repository ([data-report.pdf](./project/data-report.pdf) and [analysis-report.pdf](./project/analysis-report.pdf)) are subject to the following terms:

_Usage:_ You are free to use, share, and adapt the content of these reports for both personal and commercial purposes.

_Attribution Requirement:_ If you use or reference content from the reports, you must include a reference to this repository (e.g. the repository URL).

_Exclusions:_ These terms apply exclusively to the reports. All other content (e.g., code) in the repository is licensed separately under the MIT License.
