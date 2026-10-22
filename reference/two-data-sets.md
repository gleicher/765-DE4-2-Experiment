<!-- Source: https://pages.graphics.cs.wisc.edu/765-25/posts/two-data-sets/ -->

# A Tale of Two Data Sets in Posts September 7, 2025 (Last Modified: August 21, 2026) Data

Over the next few weeks (3 modules) we will be working with two different data sets: US Census Data and Life Expectancy around the World. This page describes the data sets and provides access to them.

Modules 2, 3 and 4 involve design exercises where you will work with “real” data sets. These assignments will involve two different data sets: a data set from the US Department of Agriculture (USDA) that provides county level aggregation of population data aggregated at the county level, and a data set of life expectancies from around the world (across many years).

There are two versions of each data set provided.

Quick links:

  - GitHub Repo: [765Data](https://github.com/uwgraphics/765Data)
  - Census CSV file (county-level): [GitHub link](https://github.com/uwgraphics/765Data/blob/main/full_census_dataset.csv)
  - Census CSV file (state-level): [GitHub link](https://github.com/uwgraphics/765Data/blob/main/aggregate_census_dataset.csv)
  - Census Readme: [README](https://github.com/uwgraphics/765Data/blob/main/census_readme.md)
  - Life Expectancy World Bank (1960-2023, broken down by sex):
      - CSV File [GitHub link](https://raw.githubusercontent.com/uwgraphics/765Data/refs/heads/main/lifespan_dataset_1960.csv)
      - Life Expectancy Readme: [README](https://github.com/uwgraphics/765Data/blob/main/lifespan_readme.md)
  - Life Expectancy [Our World in Data](https://ourworldindata.org/life-expectancy) (includes historical data):
      - CSV File [GitHub link](https://github.com/uwgraphics/765Data/blob/main/life-expectancy-owid/life-expectancy-owid.csv)
      - Readme [GitHub link](https://github.com/uwgraphics/765Data/blob/main/life-expectancy-owid/readme.md)

Looking ahead, the assignments are…

  - Module 2: [Design Exercise 2-1: Critique Practice (due Fri, Sep 26)](https://canvas.wisc.edu/courses/476055/assignments/2758531) - You’ll be asked to critique some visualizations we made that use this data. (in addition to some others)
  - Module 2: [Design Exercise 2-2: Questions and Sketches (due Fri, Sep 26)](https://canvas.wisc.edu/courses/476055/assignments/2758532) - You’ll be asked to think about what questions come up in the data, and to sketch some designs that use it.
  - Module 3: [Design Exercise 3-1: Make Pictures (due Fri, Oct 10)](https://canvas.wisc.edu/courses/476055/assignments/2758533) - You will be asked to make some visualizations using these data sets (for things specified by us).
  - Module 3: [Design Exercise 3-2: Explore (due Fri, Oct 10)](https://canvas.wisc.edu/courses/476055/assignments/2758534) - You will be asked to make some exploratory visualizations of these data sets.
  - Module 4: [Design Exercise 4-1: OPT-IN: DE4 Drafts (due Fri, Oct 17)](https://canvas.wisc.edu/courses/476055/assignments/2758536) - You will be asked to pose questions and make drafts for 4-2.
  - Module 4: [Design Exercise 4-2: Visualizations from 2 data sets (due Fri, Oct 24)](https://canvas.wisc.edu/courses/476055/assignments/2758538) - You will be asked to make several visualizations from these data sets.

## Some comments on class mechanics and data sets

For these assignments, we are forcing you to use our data sets. Hopefully, they are “general interest” enough that you are interested.

We chose these data sets because they are simple enough to work for class, but complex enough to be interesting. They are (intentionally) problematic in several ways (we don’t want to make things too easy).

In the past, we’ve only had one data set per exercise. But this time, we’re trying two. But you will work with these data sets for 6 weeks - so the time of sorting them out at the beginning will (hopefully) pay off.

We intentionally have chosen one data set in “wide” format and one in “tall” format.

Wide vs. Tall

I expect most people know this, but here is a nice explanation provided by Gemini with the prompt *You are a teaching assistant for a graduate level Data Visualization Class. Explain the difference between “wide” data and “tall” data (in terms of the tabular form that data is provided in)*

As a teaching assistant in your Data Visualization class, I’m here to clarify the fundamental difference between “wide” and “tall” data formats. Understanding this distinction is crucial because the shape of your data often dictates how easily you can create certain types of visualizations.

### The Core Difference at a Glance

In short, the distinction boils down to how you organize your variables and observations in a table.

  - **Wide data** is characterized by having each observational unit (like a person, a country, or a test subject) represented by a single row, with each measurement or variable for that unit in its own separate column. This format is often described as being more “human-readable” at a glance.

  - **Tall data** (also known as “long” data) represents each measurement for an observational unit as a separate row. This means a single observational unit will often be represented across multiple rows. This format is generally more “machine-readable” and is often the preferred format for data visualization software.

-----

### A Practical Example

Let’s consider a simple dataset tracking the sales for two products, “Product A” and “Product B,” over three years.

#### Wide Data Format

In the wide format, each year has its own row, and each product’s sales figure gets its own column.

| Year | Sales\_Product\_A | Sales\_Product\_B |
| :--- | :---------------- | :---------------- |
| 2022 | 150               | 200               |
| 2023 | 170               | 220               |
| 2024 | 180               | 250               |

You can see that the data table grows “wider” as you add more variables (in this case, more products).

#### Tall Data Format

In the tall format, we have a column to identify the product and another for its corresponding sales value.

| Year | Product   | Sales |
| :--- | :-------- | :---- |
| 2022 | Product A | 150   |
| 2022 | Product B | 200   |
| 2023 | Product A | 170   |
| 2023 | Product B | 220   |
| 2024 | Product A | 180   |
| 2024 | Product B | 250   |

Notice how the table grows “taller” as you add more observations for each year.

-----

### Why This Matters for Data Visualization

For many data visualization tools and packages (like Tableau, ggplot2 in R, or Seaborn in Python), the **tall data format is strongly preferred**. This is because it aligns with the principles of **“tidy data”**, a concept popularized by data scientist Hadley Wickham. The key principles of tidy data are:

1.  Each variable forms a column.
2.  Each observation forms a row.
3.  Each type of observational unit forms a table.

In our tall data example, `Year`, `Product`, and `Sales` are all distinct variables, and each has its own column. This structure makes it much easier to create visualizations where you want to, for example:

  - Map the `Product` variable to different colors in a line chart to compare sales over time.
  - Create faceted plots (small multiples) for each `Product`.
  - Easily filter or aggregate your data by `Product`.

With the wide format, these operations can be more cumbersome, often requiring you to manually specify each “Sales\_Product” column for plotting.

### Summary Comparison

| Feature         | Wide Data                                                     | Tall Data                                                     |
| :-------------- | :------------------------------------------------------------ | :------------------------------------------------------------ |
| **Structure**   | Each subject has one row with multiple columns for variables. | Each subject has multiple rows, one for each observation.     |
| **Readability** | Often easier for humans to scan and understand quickly.       | Can be less intuitive to read at a glance.                    |
| **Flexibility** | Adding new variables requires adding new columns.             | Adding new observations is as simple as adding new rows.      |
| **Data Viz**    | Can be less flexible for many visualization tools.            | The preferred format for most modern visualization libraries. |

As you progress in data visualization, you’ll frequently find yourself needing to reshape your data from a wide format to a tall format to make your visualization tasks easier and more efficient. This process is often referred to as “melting” or “pivoting” your data.

To make access easy, we are hosting the data sets on GitHub. (LINK)

## Census Data

This data set has a variety of data about the US, broken down by county. It has information such as population, unemployment numbers, and education levels. It covers a number of years, but for different variables, the years covered are different.

The US Department of Agriculture (USDA) provides county level aggregation of population data aggregated at the **county** level. They gather education data, income data, poverty data, and population data. Later in the semester, we might gather more detailed data from other sources. (we will also provide the data at the state level)

The USDA provides this data as 4 separate sheets, but together, they provide a very rich and complex data set full of stories. To help you get started faster (and focus on visualization, not data cleaning), the Cat (the 2025 TA) has joined the data into one “convenient” large file.

This year, please get the data (and readme) from the GitHub Repo: <https://github.com/uwgraphics/765Data/> (if you don’t have experience working with GitHub, please ask for help).

If you want to see an example of trying to work with this data in Tableau, check provide link to my Tableau tutorial look at: [Tableau Tutorial for CS765: Getting Started with Census Data](https://pages.graphics.cs.wisc.edu/VisSnacks/tutorials/tableau-tutorial/) (although, this was last year’s data and assignment).

We will also provide a tutorial on working with this data using standard Python tools. (COMING SOON\!)

## Life Expectancy Data

I was inspired to use this data set by colleagues at the University of Vienna who used it for an assignment in their class.

There are two versions of this data:

  - World Bank Data - This is only 1960 to the present, but has almost all countries for almost all years, and it is broken down by Sex.
  - [Our World in Data](https://ourworldindata.org/life-expectancy) - This data set has varying historic data at irregular intervals (there is data for some countries over hundreds of years\!), and almost all (current) countries from about 1950-present.

See the GitHub Repo: <https://github.com/uwgraphics/765Data/> for the data and a Readme.

## Final Thoughts…

Working with two datasets with different challenges will force you to think about how different tools work with data in different forms. We urge you to try using different tools over the course of the assignments. The assignments will force you to work with both data sets.

#### GenAI Disclosure:

I asked Gemini to write the difference between wide and tall data. It did a really nice job.
