import pandas as pd

from src.inventory import (
    load_inventory_data,
    get_inventory_stats,
    get_product_movement
)


def get_sustainability_data(sales_file):

    # ============================================================
    # LOAD CURRENT DATA
    # ============================================================

    inventory = load_inventory_data()

    inventory_stats = get_inventory_stats()

    movement = get_product_movement(
        sales_file
    )


    # ============================================================
    # BASIC METRICS
    # ============================================================

    total_products = inventory_stats[
        "total_products"
    ]

    low_stock = inventory_stats[
        "low_stock_items"
    ]

    critical = inventory_stats[
        "critical_alerts"
    ]

    total_categories = inventory_stats.get(
        "total_categories",
        int(
            inventory["Category"]
            .nunique()
        )
    )


    fast_moving = movement[
        "fast_moving_products"
    ]

    slow_moving = movement[
        "slow_moving_products"
    ]


    # ============================================================
    # INVENTORY EFFICIENCY
    # ============================================================

    if total_products > 0:

        healthy_products = max(
            total_products - low_stock,
            0
        )

        inventory_efficiency = round(
            (
                healthy_products
                / total_products
            )
            * 100,
            1
        )

    else:

        inventory_efficiency = 0


    # ============================================================
    # SDG 12
    # RESPONSIBLE CONSUMPTION AND PRODUCTION
    # ============================================================

    if total_products > 0:

        stock_health_score = round(
            (
                (
                    total_products
                    - critical
                )
                / total_products
            )
            * 100,
            1
        )

    else:

        stock_health_score = 0


    # ============================================================
    # DEMAND BALANCE
    # ============================================================

    movement_total = (
        fast_moving
        + slow_moving
    )

    if movement_total > 0:

        demand_balance = round(
            (
                fast_moving
                / movement_total
            )
            * 100,
            1
        )

    else:

        demand_balance = 0


    # ============================================================
    # SDG 8
    # DECENT WORK AND ECONOMIC GROWTH
    #
    # Based on:
    # - Inventory efficiency
    # - Demand balance
    # ============================================================

    sdg8_score = round(
        (
            inventory_efficiency
            +
            demand_balance
        )
        / 2,
        1
    )


    # ============================================================
    # SDG 9
    # INDUSTRY, INNOVATION AND INFRASTRUCTURE
    #
    # NOW DYNAMIC
    # ============================================================

    sdg9_components = []


    # ------------------------------------------------------------
    # 1. Inventory data availability
    # ------------------------------------------------------------

    inventory_data_available = (
        total_products > 0
    )

    if inventory_data_available:

        sdg9_components.append(25)


    # ------------------------------------------------------------
    # 2. Category-level analytics
    # ------------------------------------------------------------

    category_data_available = (
        total_categories > 0
    )

    if category_data_available:

        sdg9_components.append(25)


    # ------------------------------------------------------------
    # 3. Product movement analytics
    # ------------------------------------------------------------

    movement_data_available = (
        movement_total > 0
    )

    if movement_data_available:

        sdg9_components.append(25)


    # ------------------------------------------------------------
    # 4. Digital decision-support capability
    #
    # The system can generate:
    # - inventory alerts
    # - product movement analysis
    # - analytical insights
    # ------------------------------------------------------------

    decision_support_available = (

        total_products > 0
        and
        (
            low_stock >= 0
        )
        and
        (
            movement_total >= 0
        )

    )

    if decision_support_available:

        sdg9_components.append(25)


    if sdg9_components:

        sdg9_score = round(
            sum(sdg9_components),
            1
        )

    else:

        sdg9_score = 0


    # ============================================================
    # SDG 12
    # ============================================================

    sdg12_score = stock_health_score


    # ============================================================
    # SUSTAINABILITY INSIGHTS
    # ============================================================

    insights = []


    if low_stock > 0:

        insights.append(
            f"{low_stock} products require "
            "inventory attention."
        )


    if critical > 0:

        insights.append(
            f"{critical} products are in "
            "critical stock condition."
        )


    if slow_moving > 0:

        insights.append(
            f"{slow_moving} products show "
            "slow movement and may require "
            "inventory review to reduce "
            "potential overstock waste."
        )


    if fast_moving > 0:

        insights.append(
            f"{fast_moving} products show "
            "strong demand and should be "
            "monitored to prevent stockouts."
        )


    if inventory_efficiency >= 70:

        insights.append(
            "Inventory health is relatively "
            "stable based on current stock levels."
        )

    else:

        insights.append(
            "Inventory optimization should "
            "be prioritized to improve stock health."
        )


    # ============================================================
    # RETURN DATA
    # ============================================================

    return {

        "total_products":
            total_products,

        "total_categories":
            total_categories,

        "low_stock":
            low_stock,

        "critical":
            critical,

        "fast_moving":
            fast_moving,

        "slow_moving":
            slow_moving,

        "inventory_efficiency":
            inventory_efficiency,

        "stock_health_score":
            stock_health_score,

        "demand_balance":
            demand_balance,

        "sdg8_score":
            sdg8_score,

        "sdg9_score":
            sdg9_score,

        "sdg12_score":
            sdg12_score,

        "insights":
            insights
    }