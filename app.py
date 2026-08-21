from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

import os
import markdown
from uuid import uuid4

from src.advisor_utils import generate_ai_advice
from src.predict import predict_profit
from src.validator import validate_dataset
import pandas as pd

from flask import Flask, request, render_template

from werkzeug.utils import secure_filename

from src.dashboard import (
    get_dashboard_stats,
    generate_dashboard_charts
)


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)


# ============================================================
# FILE PATH
# ============================================================

UPLOAD_FOLDER = "static/uploads"

LATEST_FILE = os.path.join(
    UPLOAD_FOLDER,
    "latest.csv"
)


# ============================================================
# CREATE REQUIRED FOLDERS
# ============================================================

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    "static/images",
    exist_ok=True
)


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

    # --------------------------------------------------------
    # CHECK LATEST DATASET
    # --------------------------------------------------------

    if not os.path.exists(
        LATEST_FILE
    ):

        stats = {

            "total_sales": 0,

            "total_profit": 0,

            "total_orders": 0

        }

        charts = []

        advice_html = """
        <h3>Getting Started</h3>

        <ul>
            <li>
                Upload a valid retail CSV dataset.
            </li>

            <li>
                SmartRetail will validate the dataset.
            </li>

            <li>
                ML prediction and visual analytics
                will be generated automatically.
            </li>

            <li>
                The AI Advisor will then generate
                business recommendations.
            </li>
        </ul>
        """

        return render_template(

            "owner.html",

            stats=stats,

            charts=charts,

            advice=advice_html

        )


    # ========================================================
    # LOAD DASHBOARD DATA
    # ========================================================

    try:

        stats = get_dashboard_stats(
            LATEST_FILE
        )

    except Exception as error:

        print(
            "Dashboard statistics error:",
            error
        )

        stats = {

            "total_sales": 0,

            "total_profit": 0,

            "total_orders": 0

        }


    # ========================================================
    # GENERATE CHARTS
    # ========================================================

    try:

        charts = generate_dashboard_charts(
            LATEST_FILE
        )

    except Exception as error:

        print(
            "Chart generation error:",
            error
        )

        charts = []


    # ========================================================
    # GENERATE AI ADVICE
    # ========================================================

    try:

        advice = generate_ai_advice(
            stats
        )

        advice_html = markdown.markdown(
            advice,
            extensions=[
                "extra"
            ]
        )

    except Exception as error:

        print(
            "AI Advisor error:",
            error
        )

        advice_html = """
        <h3>AI Advisor</h3>

        <ul>
            <li>
                AI recommendations could not be
                generated at this time.
            </li>

            <li>
                Dashboard analytics are still available.
            </li>
        </ul>
        """


    # ========================================================
    # RENDER DASHBOARD
    # ========================================================

    return render_template(

        "owner.html",

        stats=stats,

        charts=charts,

        advice=advice_html

    )


# ============================================================
# PREDICTION
# ============================================================

@app.route("/prediction", methods=["GET", "POST"])
def prediction():

    # Default values shown when page is opened
    predicted_profit = None
    model_name = None
    r2_score = None
    mae = None
    rmse = None
    error = None
    success = None

    # ==============================
    # GET REQUEST
    # ==============================

    if request.method == "GET":

        return render_template(
            "prediction.html",
            predicted_profit=None,
            model_name=None,
            r2_score=None,
            mae=None,
            rmse=None,
            error=None,
            success=None
        )


    # ==============================
    # POST REQUEST
    # ==============================

    if request.method == "POST":

        try:

            # --------------------------------
            # Check uploaded file
            # --------------------------------

            if "file" not in request.files:

                raise ValueError(
                    "No file was uploaded."
                )

            file = request.files["file"]


            if file.filename == "":

                raise ValueError(
                    "Please select a CSV file."
                )


            if not file.filename.lower().endswith(".csv"):

                raise ValueError(
                    "Only CSV files are supported."
                )


            # --------------------------------
            # Create upload folder
            # --------------------------------

            upload_folder = os.path.join(
                app.root_path,
                "static",
                "uploads"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )


            # --------------------------------
            # Save uploaded CSV
            # --------------------------------

            filename = secure_filename(
                file.filename
            )

            temporary_filepath = os.path.join(
                upload_folder,
                f".upload-{uuid4().hex}-{filename}"
            )

            file.save(temporary_filepath)


            # --------------------------------
            # Validate CSV before replacing the
            # dataset used by the dashboard.
            # --------------------------------

            is_valid, validation_data, missing_optional = (
                validate_dataset(temporary_filepath)
            )

            if not is_valid:

                raise ValueError(
                    "Missing required columns: "
                    + ", ".join(validation_data)
                )

            df = validation_data


            if df.empty:

                raise ValueError(
                    "The uploaded CSV is empty."
                )


            # --------------------------------
            # Publish the validated upload as
            # the dataset used by /owner.
            # --------------------------------

            os.replace(
                temporary_filepath,
                LATEST_FILE
            )


            # --------------------------------
            # Run prediction
            # --------------------------------

            from src.predict import predict_profit

            result = predict_profit(LATEST_FILE)


            # --------------------------------
            # Handle prediction result
            # --------------------------------

            if isinstance(result, dict):

                predicted_profit = result.get(
                    "predicted_profit"
                )

                model_name = (
                    result.get("model_name")
                    or result.get("model")
                    or "Unknown"
                )

                r2_score = result.get(
                    "r2_score"
                )

                mae = result.get(
                    "mae"
                )

                rmse = result.get(
                    "rmse"
                )

            else:

                predicted_profit = result

                model_name = "Linear Regression"


            # --------------------------------
            # Format values
            # --------------------------------

            if predicted_profit is not None:

                try:

                    predicted_profit = round(
                        float(predicted_profit),
                        2
                    )

                except:

                    pass


            success = (
                f"Prediction completed successfully "
                f"for {len(df)} records."
            )


        except Exception as e:

            error = str(e)

            print(
                "\n========== PREDICTION ERROR =========="
            )

            print(error)

            print(
                "======================================\n"
            )


    # --------------------------------
    # Return page
    # --------------------------------

    return render_template(
        "prediction.html",

        predicted_profit=predicted_profit,

        model_name=model_name,

        r2_score=r2_score,

        mae=mae,

        rmse=rmse,

        error=error,

        success=success
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
