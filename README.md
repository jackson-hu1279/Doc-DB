# Doc DB

A Python script designed to automate the collection of specified doctor profile and clinic information from the Hong Kong government's [Primary Care Directory](https://apps.pcdirectory.gov.hk/Public/TC) website. This tool aims to streamline the data collection process by automatically retrieving and organising the essential healthcare provider details into a structured format.

## Preparation

1. Have a working Python environment
2. Install required packages specified in `requirements.txt`
3. Follow the `.env.example` template to create a `.env` with cookie values
4. Create a `doc_names.xlsx` Excel file under the `input_output` directory following the `doc_names_sample.xlsx` template
5. Add a list of doctor names you intend to search under the `name` column in `doc_names.xlsx`

## Usage

Once complete all steps for preparation and specify a list of doctor names in the input Excel file, you can either execute the Python script or run blocks of code step by step in the given Jupyter Notebook.

### 1. Python Script

```python
python doc_collector.py
```

### 2. Jupyter Notebook

Open the `doc_collector_notebook.ipynb` and execute blocks of code.

## Screenshots
