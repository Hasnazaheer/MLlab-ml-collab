# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Titanic Dataset — Exploratory Data Analysis
#
# This notebook explores the Titanic dataset used for the ML collaboration project.
#
# The goal is to understand the dataset structure, missing values, target distribution, important passenger features, and relationships that may be useful for later model development.
#
# **Dataset:** Titanic `train.csv` and `test.csv`
#

# %% [markdown]
# ## 1. Load Libraries and Data

# %%
import pandas as pd
import matplotlib.pyplot as plt

# Load the Titanic data using project-relative paths.
train_df = pd.read_csv("../data/raw/train.csv")
test_df = pd.read_csv("../data/raw/test.csv")

print("Training shape:", train_df.shape)
print("Test shape:", test_df.shape)


# %% [markdown]
# ## 2. Understand the Dataset

# %%
# Preview the training data
train_df.head()


# %%
# Column names
print("Training columns:")
print(train_df.columns.tolist())


# %%
# Data types and non-null counts
train_df.info()


# %%
# Numerical summary
train_df.describe()


# %% [markdown]
# ### Initial observations
#
# Use the outputs above to describe:
# - the number of rows and columns,
# - the available passenger features,
# - the data types,
# - and the numerical ranges.
#
# These observations should be based on the actual dataset output.
#

# %% [markdown]
# ## 3. Check Missing Values

# %%
# Number of missing values in each column
missing_counts = train_df.isnull().sum()
missing_counts


# %%
# Percentage of missing values
missing_percent = (train_df.isnull().mean() * 100).sort_values(ascending=False)
missing_percent


# %%
# Visualize missing-value counts
missing_counts[missing_counts > 0].sort_values(ascending=False).plot(kind="bar")
plt.title("Missing Values by Column")
plt.xlabel("Column")
plt.ylabel("Number of Missing Values")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# %% [markdown]
# ### Missing-value observations
#
# Record which columns contain missing values and consider how this may affect preprocessing in the later ML pipeline.
#
# Do not perform the final preprocessing here; this notebook is for exploration.
#

# %% [markdown]
# ## 4. Explore the Target Variable

# %%
# Target distribution
train_df["Survived"].value_counts()


# %%
# Target proportions
train_df["Survived"].value_counts(normalize=True)


# %%
# Visualize survival counts
train_df["Survived"].value_counts().plot(kind="bar")
plt.title("Titanic Survival Distribution")
plt.xlabel("Survived (0 = No, 1 = Yes)")
plt.ylabel("Number of Passengers")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# %% [markdown]
# ### Target observations
#
# Describe the balance between passengers who survived and those who did not.
#
# Use the numerical output rather than assuming the classes are balanced.
#

# %% [markdown]
# ## 5. Explore Important Features

# %% [markdown]
# ### Passenger class

# %%
train_df["Pclass"].value_counts().sort_index()


# %%
# Survival rate by passenger class
train_df.groupby("Pclass")["Survived"].mean()


# %%
train_df.groupby("Pclass")["Survived"].mean().plot(kind="bar")
plt.title("Survival Rate by Passenger Class")
plt.xlabel("Passenger Class")
plt.ylabel("Survival Rate")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# %% [markdown]
# ### Sex

# %%
train_df["Sex"].value_counts()


# %%
# Survival rate by sex
train_df.groupby("Sex")["Survived"].mean()


# %%
train_df.groupby("Sex")["Survived"].mean().plot(kind="bar")
plt.title("Survival Rate by Sex")
plt.xlabel("Sex")
plt.ylabel("Survival Rate")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# %% [markdown]
# ### Age

# %%
train_df["Age"].describe()


# %%
train_df["Age"].plot(kind="hist", bins=20)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Passengers")
plt.tight_layout()
plt.show()


# %% [markdown]
# ### Fare

# %%
train_df["Fare"].describe()


# %%
train_df["Fare"].plot(kind="hist", bins=30)
plt.title("Fare Distribution")
plt.xlabel("Fare")
plt.ylabel("Number of Passengers")
plt.tight_layout()
plt.show()


# %% [markdown]
# ### Family-related features

# %%
# Inspect family-related variables
train_df[["SibSp", "Parch"]].describe()


# %%
# Survival rate by number of siblings/spouses aboard
train_df.groupby("SibSp")["Survived"].mean()


# %%
# Survival rate by number of parents/children aboard
train_df.groupby("Parch")["Survived"].mean()


# %% [markdown]
# ## 6. Additional Visualizations

# %%
# Survival counts by passenger class
pd.crosstab(train_df["Pclass"], train_df["Survived"]).plot(kind="bar")
plt.title("Survival Counts by Passenger Class")
plt.xlabel("Passenger Class")
plt.ylabel("Number of Passengers")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# %%
# Survival counts by sex
pd.crosstab(train_df["Sex"], train_df["Survived"]).plot(kind="bar")
plt.title("Survival Counts by Sex")
plt.xlabel("Sex")
plt.ylabel("Number of Passengers")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# %%
# Survival by sex and passenger class
survival_by_sex_class = train_df.pivot_table(
    values="Survived", index="Pclass", columns="Sex", aggfunc="mean"
)
survival_by_sex_class


# %%
survival_by_sex_class.plot(kind="bar")
plt.title("Survival Rate by Sex and Passenger Class")
plt.xlabel("Passenger Class")
plt.ylabel("Survival Rate")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# %% [markdown]
# ## 7. Initial Observations
#
# After running the notebook, summarize the main findings from the actual outputs.
#
# Suggested points to address:
#
# 1. What is the size and structure of the training dataset?
# 2. Which columns have missing values?
# 3. How is the `Survived` target distributed?
# 4. Does survival appear to vary by passenger class?
# 5. Does survival appear to vary by sex?
# 6. What do the age and fare distributions look like?
# 7. Which features may require preprocessing before model training?
#
# **Important:** Replace or expand these points with observations supported by your actual results.
#

# %% [markdown]
# ## 8. Reusable Project Function
#
# The assignment requires one reusable cleaning or feature function to live in `src/` with a unit test in `tests/`.
#
# After creating that function, import it here instead of keeping reusable logic only inside the notebook.
#
# Example:
#
# ```python
# from src.preprocessing import missing_value_counts
#
# missing_value_counts(train_df)
# ```
#
# The exact function should match the implementation you create in `src/`.
#

# %% [markdown]
# ## Conclusion
#
# This EDA provides an initial understanding of the Titanic dataset and identifies data-quality and feature patterns that should be considered during the reproducible preparation and training pipeline in the next phase.
#
