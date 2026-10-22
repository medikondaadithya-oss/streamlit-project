import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="CSV Data Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("Upload CSV and Analyze")
st.write("Upload a CSV file to preview, filter, sort, and analyze your data.")

# Upload CSV file
file = st.file_uploader("Upload a CSV file", type=["csv"])

if file is not None:
    try:
        # Read CSV file
        df = pd.read_csv(file)

        # Clean column names and text values
        df.columns = df.columns.str.strip()

        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].str.strip()

        if df.empty:
            st.warning("The uploaded CSV file is empty.")

        else:
            # Data Preview
            st.subheader("1. Data Preview")
            st.dataframe(df, use_container_width=True)

            st.write("Rows:", df.shape[0])
            st.write("Columns:", df.shape[1])

            # Missing Values
            st.subheader("2. Missing Values")
            st.dataframe(
                df.isnull().sum().rename("Missing Values").to_frame()
            )

            option = st.radio(
                "Handle missing values:",
                ["Keep", "Drop", "Fill with 0"],
                horizontal=True
            )

            if option == "Drop":
                df = df.dropna()

            elif option == "Fill with 0":
                df = df.fillna(0)

            st.subheader("3. Processed Data")
            st.dataframe(df, use_container_width=True)

            # Statistics
            st.subheader("4. Statistics")
            st.dataframe(
                df.describe(include="all"),
                use_container_width=True
            )

            # Filter by Column
            st.subheader("5. Filter by Column")

            col = st.selectbox("Choose column", df.columns)
            value = st.text_input("Enter filter value")

            if value:
                filtered = df[
                    df[col]
                    .astype("string")
                    .str.contains(
                        value,
                        case=False,
                        na=False,
                        regex=False
                    )
                ]

                st.write("Filtered Results")
                st.dataframe(filtered, use_container_width=True)

            # Sort Data
            st.subheader("6. Sort Data")

            sort_col = st.selectbox(
                "Sort by column",
                df.columns,
                key="sort_col"
            )

            ascending = st.checkbox("Ascending order", value=True)

            sorted_df = df.sort_values(
                by=sort_col,
                ascending=ascending,
                na_position="last"
            )

            st.dataframe(sorted_df, use_container_width=True)

            # Download CSV
            st.subheader("7. Download Processed CSV")

            csv_data = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="processed.csv",
                mime="text/csv"
            )

            # Group By and Aggregate
            st.subheader("8. Group By and Aggregate")

            group_col = st.selectbox(
                "Choose grouping column",
                df.columns,
                key="group_col"
            )

            num_cols = [
                c for c in df.select_dtypes(include="number").columns
                if c != group_col
            ]

            if num_cols:
                agg_func = st.selectbox(
                    "Choose aggregation",
                    ["mean", "sum", "min", "max", "count"]
                )

                result = df.groupby(group_col)[num_cols].agg(agg_func)

                st.dataframe(result, use_container_width=True)

            else:
                st.info("No numeric columns are available to aggregate.")

    except Exception as e:
        st.error(f"Error reading the CSV file: {e}")

else:
    st.info("Please upload a CSV file to begin.")

