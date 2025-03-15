import io

import pandas as pd
import streamlit as st

from search import get_solution


def main():
    st.title("Curtin Timetable Picker")
    st.write("Developed with ❤️ by Ren Jie")
    st.write(
        "Paste values in the format: Module, Class, Lecture, Tutorial (tab-separated)"
    )
    st.write(
        "Lecture and Tutorial Format is day, start_time , end_time. e.g. Mon 1030am to 1230pm"
    )

    num_combi = st.number_input("Number of Combination", min_value=0, value=4)

    # Initialize session state for the DataFrame
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(
            columns=["Module", "Class", "Lecture", "Tutorial"]
        )

    # Text area for pasting tabular data
    pasted_data = st.text_area("Paste data here (tab-separated):", height=200)

    # Convert pasted data to DataFrame
    if pasted_data:
        rows = [line.split("\t") for line in pasted_data.strip().split("\n")]
        st.session_state.df = pd.DataFrame(
            rows, columns=["Module", "Class", "Lecture", "Tutorial"]
        )

    # Display the editable table
    edited_df = st.data_editor(
        st.session_state.df, num_rows="dynamic", use_container_width=True
    )

    # Save changes
    st.session_state.df = edited_df

    # Button to run the solution
    if st.button("Run"):
        result_df = get_solution(edited_df, num_combi)
        st.session_state.solution_df = (
            result_df  # Store solution in session state
        )

        # Show result if available
        st.write("Generated Schedule:")
        st.dataframe(result_df)

    # Download button
    if "solution_df" in st.session_state:
        csv_buffer = io.StringIO()
        st.session_state.solution_df.to_csv(csv_buffer, index=False)
        st.download_button(
            "Download Solution",
            csv_buffer.getvalue(),
            "table_data.csv",
            "text/csv",
        )


if __name__ == "__main__":
    main()
