from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)
from flask import request, jsonify

import os
import markdown
from functools import wraps
from uuid import uuid4
from src.chatbot import ask_groq
import json

from config import Config
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
from src.inventory import (
    get_inventory_stats,
    load_inventory_data,
    get_reorder_alerts,
    get_product_movement,
    get_inventory_chart_data
)
from src.sustainability import (
    get_sustainability_data
)
from src.sales_analytics import (
    get_sales_analytics
)


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)
app.config.from_object(
    Config
)


# ============================================================
# AUTHENTICATION
# ============================================================

USERS = {

    "owner": {

        "password": "owner123",

        "role": "owner"

    },

    "inventory": {

        "password": "inventory123",

        "role": "inventory_manager"

    }

}


def require_roles(*allowed_roles):

    def decorator(view_function):

        @wraps(view_function)
        def wrapped_view(*args, **kwargs):

            role = session.get(
                "role"
            )

            if role not in allowed_roles:

                return redirect(
                    url_for("login")
                )

            return view_function(
                *args,
                **kwargs
            )

        return wrapped_view

    return decorator


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
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if session.get("role") == "owner":

        return redirect(
            url_for("owner")
        )

    if session.get("role") == "inventory_manager":

        return redirect(
            url_for("inventory")
        )

    error = None

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        user = USERS.get(username)

        if user and password == user["password"]:

            session.clear()

            session["username"] = username

            session["role"] = user["role"]

            if user["role"] == "owner":

                return redirect(
                    url_for("owner")
                )

            return redirect(
                url_for("inventory")
            )

        error = "Invalid username or password."

    return render_template(
        "login.html",
        error=error,
        inventory_access=False
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# ============================================================
# INVENTORY
# ============================================================

@app.route("/inventory")
@require_roles("owner", "inventory_manager")
def inventory():

    inventory_stats = get_inventory_stats()

    reorder_alerts = get_reorder_alerts()

    movement_stats = get_product_movement(
        LATEST_FILE
    )

    inventory_chart_data = get_inventory_chart_data()

    return render_template(
        "inventory.html",
        total_products=inventory_stats["total_products"],
        low_stock_items=inventory_stats["low_stock_items"],
        critical_alerts=inventory_stats["critical_alerts"],
        total_categories=inventory_stats["total_categories"],
        fast_moving_products=movement_stats[
            "fast_moving_products"
        ],
        slow_moving_products=movement_stats[
            "slow_moving_products"
        ],
        reorder_alerts=reorder_alerts,
        inventory_chart_data=inventory_chart_data
    )
# ============================================================
# SUSTAINABILITY / SDG DASHBOARD
# ============================================================

@app.route("/sustainability")
@require_roles("owner", "inventory_manager")
def sustainability():

    try:

        sustainability_data = (
            get_sustainability_data(
                LATEST_FILE
            )
        )

        return render_template(
            "sustainability.html",
            data=sustainability_data
        )

    except Exception as error:

        print(
            "Sustainability dashboard error:",
            error
        )

        return render_template(
            "sustainability.html",
            data={
                "total_products": 0,
                "total_categories": 0,
                "low_stock": 0,
                "critical": 0,
                "fast_moving": 0,
                "slow_moving": 0,
                "inventory_efficiency": 0,
                "stock_health_score": 0,
                "demand_balance": 0,
                "sdg8_score": 0,
                "sdg9_score": 0,
                "sdg12_score": 0,
                "insights": [
                    "Sustainability data could not be loaded."
                ]
            }
        )
# ============================================================
# SALES ANALYTICS
# ============================================================

@app.route("/sales-analytics")
@require_roles("owner", "inventory_manager")
def sales_analytics():

    try:

        analytics_data = get_sales_analytics(
            LATEST_FILE
        )

        return render_template(
            "sales_analytics.html",
            data=analytics_data
        )

    except Exception as error:

        print(
            "Sales analytics error:",
            error
        )

        return render_template(
            "sales_analytics.html",
            data={
                "total_sales": 0,
                "total_profit": 0,
                "total_quantity": 0,
                "total_records": 0,
                "average_sale": 0,
                "profit_margin": 0,
                "average_discount": 0,

                "category_sales": [],
                "category_profit": [],
                "category_quantity": [],

                "sales_trend": [],
                "profit_trend": [],

                "product_performance": [],

                "best_sales_category": "N/A",
                "best_sales_value": 0,

                "best_profit_category": "N/A",
                "best_profit_value": 0,

                "top_product": "N/A",
                "top_product_sales": 0,

                "insights": [
                    "Sales analytics data could not be loaded."
                ]
            }
        )


# ============================================================
# ADD PRODUCT
# ============================================================

# ============================================================
# ADD PRODUCT
# ============================================================

@app.route("/inventory/add", methods=["POST"])
@require_roles("owner", "inventory_manager")
def add_product():

    try:

        # --------------------------------------------------------
        # INVENTORY DATASET
        # IMPORTANT:
        # Do NOT use LATEST_FILE here.
        # LATEST_FILE is the sales/prediction dataset.
        # --------------------------------------------------------

        inventory_file = os.path.join(
            "data",
            "raw",
            "inventory.csv"
        )

        if not os.path.exists(
            inventory_file
        ):

            raise ValueError(
                "Inventory dataset was not found."
            )

        # --------------------------------------------------------
        # GET FORM DATA
        # --------------------------------------------------------

        product_id = request.form.get(
            "product_id",
            ""
        ).strip()

        product_name = request.form.get(
            "product_name",
            ""
        ).strip()

        category = request.form.get(
            "category",
            ""
        ).strip()

        current_stock = request.form.get(
            "current_stock",
            ""
        ).strip()

        reorder_level = request.form.get(
            "reorder_level",
            ""
        ).strip()

        unit_price = request.form.get(
            "unit_price",
            ""
        ).strip()

        supplier = request.form.get(
            "supplier",
            ""
        ).strip()

        # --------------------------------------------------------
        # REQUIRED FIELD VALIDATION
        # --------------------------------------------------------

        if not all(
            [
                product_id,
                product_name,
                category,
                current_stock,
                reorder_level,
                unit_price,
                supplier
            ]
        ):

            raise ValueError(
                "Please fill in all product fields."
            )

        # --------------------------------------------------------
        # LOAD INVENTORY CSV
        # --------------------------------------------------------

        inventory = pd.read_csv(
            inventory_file
        )

        inventory.columns = (
            inventory.columns
            .astype(str)
            .str.strip()
        )

        required_columns = [
            "Product ID",
            "Product Name",
            "Category",
            "Current Stock",
            "Reorder Level",
            "Unit Price",
            "Supplier",
            "Last Updated"
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in inventory.columns
        ]

        if missing_columns:

            raise ValueError(
                "Inventory CSV is missing columns: "
                +
                ", ".join(
                    missing_columns
                )
            )

        # --------------------------------------------------------
        # DUPLICATE PRODUCT CHECK
        # --------------------------------------------------------

        existing_ids = (
            inventory["Product ID"]
            .astype(str)
            .str.strip()
            .tolist()
        )

        if product_id in existing_ids:

            raise ValueError(
                f"Product ID '{product_id}' already exists."
            )

        # --------------------------------------------------------
        # CONVERT NUMERIC VALUES
        # --------------------------------------------------------

        try:

            stock = int(
                current_stock
            )

            reorder = int(
                reorder_level
            )

            price = float(
                unit_price
            )

        except ValueError:

            raise ValueError(
                "Current Stock and Reorder Level "
                "must be whole numbers, and Unit Price "
                "must be a valid number."
            )

        # --------------------------------------------------------
        # VALIDATE NUMERIC VALUES
        # --------------------------------------------------------

        if stock < 0:

            raise ValueError(
                "Current Stock cannot be negative."
            )

        if reorder < 0:

            raise ValueError(
                "Reorder Level cannot be negative."
            )

        if price < 0:

            raise ValueError(
                "Unit Price cannot be negative."
            )

        # --------------------------------------------------------
        # CREATE NEW INVENTORY RECORD
        # --------------------------------------------------------

        new_product = {
            "Product ID": product_id,
            "Product Name": product_name,
            "Category": category,
            "Current Stock": stock,
            "Reorder Level": reorder,
            "Unit Price": price,
            "Supplier": supplier,
            "Last Updated": pd.Timestamp.now().strftime(
                "%Y-%m-%d"
            )
        }

        # --------------------------------------------------------
        # ADD PRODUCT
        # --------------------------------------------------------

        inventory = pd.concat(
            [
                inventory,
                pd.DataFrame(
                    [new_product]
                )
            ],
            ignore_index=True
        )

        # --------------------------------------------------------
        # SAVE INVENTORY DATASET
        # --------------------------------------------------------

        inventory.to_csv(
            inventory_file,
            index=False
        )

        # --------------------------------------------------------
        # RETURN TO INVENTORY DASHBOARD
        # --------------------------------------------------------

        return redirect(
            url_for(
                "inventory",
                added="1"
            )
        )

    except Exception as error:

        return redirect(
            url_for(
                "inventory",
                error=str(error)
            )
        )
@app.route("/chatbot", methods=["POST"])
@require_roles("owner", "inventory_manager")
def chatbot():

    try:

        data = request.get_json() or {}

        message = data.get("message", "").strip()

        conversation = data.get("conversation", [])


        # Check message

        if not message:

            return jsonify({
                "success": False,
                "error": "Please enter a message."
            }), 400


        # Ask Groq AI

        response = ask_groq(
            message,
            conversation
        )


        # Return AI response

        return jsonify({
            "success": True,
            "response": response
        })


    except Exception as error:

        print(
            "Chatbot route error:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                "Something went wrong while "
                "processing your request."

        }), 500



# ============================================================
# OWNER DASHBOARD
# ============================================================

@app.route("/owner")
@require_roles("owner")
def owner():

    # --------------------------------------------------------
    # LOAD INVENTORY STATISTICS
    # --------------------------------------------------------

    try:
        inventory_stats = get_inventory_stats()

    except Exception as error:
        print(
            "Inventory statistics error:",
            error
        )

        inventory_stats = {
            "total_products": 0,
            "low_stock_items": 0,
            "critical_alerts": 0
        }

    # --------------------------------------------------------
    # CHECK LATEST DATASET
    # --------------------------------------------------------

    if not os.path.exists(
        LATEST_FILE
    ):

        stats = {

            "total_sales": 0,

            "total_profit": 0,

            "total_orders": 0,

            "r2_score": None,

            "r2_percentage": None,

            "model_name": None

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

            advice=advice_html,

            inventory_stats=inventory_stats

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

            "total_orders": 0,

            "r2_score": None,

            "r2_percentage": None,

            "model_name": None

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

        advice=advice_html,

        inventory_stats=inventory_stats

    )


# ============================================================
# PREDICTION
# ============================================================

@app.route("/prediction", methods=["GET", "POST"])
@require_roles("owner")
def prediction():

    # Default values shown when page is opened
    actual_profit = None
    predicted_profit = None
    difference = None
    deviation_percentage = None
    comparison_chart = None
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
            actual_profit=None,
            predicted_profit=None,
            difference=None,
            deviation_percentage=None,
            comparison_chart=None,
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

            # ------------------------------------------------
            # SAVE LATEST PREDICTION METRICS
            # ------------------------------------------------

            prediction_metrics_file = os.path.join(
                app.root_path,
                "static",
                "uploads",
                "prediction_metrics.json"
            )

            if isinstance(result, dict):

                prediction_metrics = {
                    "r2_score": result.get("r2_score"),
                    "r2_percentage": result.get("r2_percentage"),
                    "mae": result.get("mae"),
                    "rmse": result.get("rmse"),
                    "actual_profit": result.get("actual_profit"),
                    "predicted_profit": result.get("predicted_profit")
                }

                with open(
                    prediction_metrics_file,
                    "w",
                    encoding="utf-8"
                ) as metrics_file:

                    json.dump(
                        prediction_metrics,
                        metrics_file,
                        indent=4
                    )


            # --------------------------------
            # Handle prediction result
            # --------------------------------

            if isinstance(result, dict):

                actual_profit = result.get("actual_profit")

                predicted_profit = result.get(
                    "predicted_profit"
                )

                difference = result.get("difference")

                deviation_percentage = result.get("deviation_percentage")

                comparison_chart = result.get("comparison_chart")

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
                actual_profit = None
                difference = None
                deviation_percentage = None
                comparison_chart = None

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

        actual_profit=actual_profit,

        predicted_profit=predicted_profit,

        difference=difference,

        deviation_percentage=deviation_percentage,

        comparison_chart=comparison_chart,

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
