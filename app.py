from flask import Flask, render_template, request
import os

from src.predict import predict_profit
from src.validator import validate_dataset

from src.dashboard import (
    get_dashboard_stats,
    generate_dashboard_charts
)


app = Flask(__name__)


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# OWNER DASHBOARD
# ============================================================

@app.route("/owner")
def owner():

    filepath = "static/uploads/latest.csv"


    if os.path.exists(filepath):

        # --------------------------------------------
        # GET DATASET STATISTICS
        # --------------------------------------------

        stats = get_dashboard_stats(
            filepath
        )


        # --------------------------------------------
        # GENERATE DYNAMIC CHARTS
        # --------------------------------------------

        charts = generate_dashboard_charts(
            filepath
        )


    else:

        stats = {

            "total_sales": 0,

            "total_profit": 0,

            "total_orders": 0

        }


        charts = []


    return render_template(

        "owner.html",

        stats=stats,

        charts=charts

    )


# ============================================================
# PREDICTION
# ============================================================

@app.route(
    "/prediction",
    methods=["GET", "POST"]
)
def prediction():


    if request.method == "POST":


        dataset = request.files.get(
            "dataset"
        )


        # --------------------------------------------
        # CHECK FILE
        # --------------------------------------------

        if not dataset:

            return render_template(

                "prediction.html",

                error=
                "Please upload a CSV dataset."

            )


        # --------------------------------------------
        # SAVE DATASET
        # --------------------------------------------

        filepath = (
            "static/uploads/latest.csv"
        )


        dataset.save(
            filepath
        )


        print(
            "Uploaded:",
            filepath
        )


        # --------------------------------------------
        # VALIDATE DATASET
        # --------------------------------------------

        is_valid, result, missing_optional = (
            validate_dataset(filepath)
        )


        if not is_valid:

            return render_template(

                "prediction.html",

                error=
                f"Missing Required Columns: "
                f"{', '.join(result)}"

            )


        # --------------------------------------------
        # RUN ML PREDICTION
        # --------------------------------------------

        predicted_profit = predict_profit(
            filepath
        )


        # --------------------------------------------
        # GENERATE DASHBOARD CHARTS
        # --------------------------------------------

        generate_dashboard_charts(
            filepath
        )


        # --------------------------------------------
        # SHOW RESULT
        # --------------------------------------------

        return render_template(

            "prediction.html",

            predicted_profit=
                f"${predicted_profit:,.2f}",

            warning=(

                f"Optional Columns Missing: "
                f"{', '.join(missing_optional)}"

                if missing_optional

                else None

            )

        )


    return render_template(
        "prediction.html"
    )


# ============================================================
# RUN FLASK
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )