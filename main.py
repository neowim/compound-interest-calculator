import datetime
from dateutil.relativedelta import relativedelta
import flet
from flet import (
    Page,
    Text,
    TextField,
    ElevatedButton,
    Column,
    Row,
    DataTable,
    DataColumn,
    DataRow,
    DataCell,
    DatePicker,
    SnackBar,
    Container,
    icons,
    padding,
)
import locale

# Set locale for number formatting
locale.setlocale(locale.LC_ALL, "nl_NL.UTF-8")


def format_currency(value):
    # Format the number manually with thousands separator and 2 decimals
    formatted_value = f"{value:,.2f}"
    # Replace default separators (commas and periods) for European style
    formatted_value = (
        formatted_value.replace(",", "X").replace(".", ",").replace("X", ".")
    )
    return f"€{formatted_value}"


def main(page: Page):
    page.title = "Compound Interest Calculator"
    page.scroll = "auto"

    # Create DatePicker instances with proper configuration
    start_date_picker = DatePicker(
        first_date=datetime.datetime(2000, 1, 1),
        last_date=datetime.datetime(2050, 12, 31),
    )
    end_date_picker = DatePicker(
        first_date=datetime.datetime(2000, 1, 1),
        last_date=datetime.datetime(2050, 12, 31),
    )

    # Add DatePickers to the page
    page.overlay.append(start_date_picker)
    page.overlay.append(end_date_picker)

    # Create TextField wrappers for the DatePickers
    start_date_field = TextField(
        label="Start Date",
        icon=icons.DATE_RANGE,
        width=300,
        read_only=True,
        hint_text="Click to select start date",
        on_click=lambda _: start_date_picker.pick_date(),
    )
    end_date_field = TextField(
        label="End Date",
        icon=icons.DATE_RANGE,
        width=300,
        read_only=True,
        hint_text="Click to select end date",
        on_click=lambda _: end_date_picker.pick_date(),
    )

    def update_start_date(e):
        start_date_field.value = e.control.value.strftime("%Y-%m-%d")
        start_date_field.error_text = None
        page.update()

    def update_end_date(e):
        end_date_field.value = e.control.value.strftime("%Y-%m-%d")
        end_date_field.error_text = None
        page.update()

    # Set up on_change event handlers
    start_date_picker.on_change = update_start_date
    end_date_picker.on_change = update_end_date

    # Define global variables for controls
    initial_amount_input = TextField(
        label="Initial Amount (€)",
        width=300,
        value="1000",
        keyboard_type="number",
    )
    annual_interest_input = TextField(
        label="Annual Interest Rate (%)",
        width=300,
        value="6.0",
        keyboard_type="number",
    )
    monthly_contribution_input = TextField(
        label="Monthly Contribution (€)",
        width=300,
        value="100",
        keyboard_type="number",
    )
    calculate_button = ElevatedButton(
        "Calculate", on_click=lambda e: calculate()
    )

    # Output Texts
    total_interest_text = Text(
        value="Total Interest Earned: €0.00", size=16, weight="bold"
    )
    final_balance_text = Text(
        value="Final Savings Amount: €0.00", size=16, weight="bold"
    )

    # DataTable for Monthly Breakdown
    breakdown_table = DataTable(
        columns=[
            DataColumn(Text("Month")),
            DataColumn(Text("Interest Earned (€)")),
            DataColumn(Text("Contribution (€)")),
            DataColumn(Text("End Balance (€)")),
        ],
        rows=[],
        width=800,
        height=400,
    )

    # Function to calculate compound interest
    def calculate():
        try:
            if not start_date_picker.value or not end_date_picker.value:
                raise ValueError("Please select both start and end dates.")

            # Convert datetime objects to date objects
            start_date = start_date_picker.value.date()
            end_date = end_date_picker.value.date()

            if end_date < start_date:
                raise ValueError("End date must be after start date.")

            # Convert TextField values to float, handling empty or invalid inputs
            try:
                initial_principal = float(initial_amount_input.value or 0)
                annual_interest_rate = float(annual_interest_input.value or 0)
                monthly_contribution = float(
                    monthly_contribution_input.value or 0
                )
            except (TypeError, ValueError):
                raise ValueError("Please enter valid numeric values.")

            if (
                initial_principal < 0
                or annual_interest_rate < 0
                or monthly_contribution < 0
            ):
                raise ValueError(
                    "Please enter non-negative values for amounts and rates."
                )

            # Calculate monthly interest rate
            monthly_rate = annual_interest_rate / 100 / 12

            # Initialize variables
            balance = initial_principal
            total_interest = 0.0

            # Prepare list to store monthly data
            data = []

            # Initialize current date to the first of the start month
            current_date = start_date.replace(day=1)
            last_date_of_investment = end_date

            def get_first_day_of_month(date):
                return date.replace(day=1)

            # Iterate through each month until the end date
            while current_date <= last_date_of_investment:
                # Calculate days in the month
                last_day_of_current_month = (
                    get_first_day_of_month(current_date)
                    + relativedelta(months=1)
                    - datetime.timedelta(days=1)
                )
                total_days_in_month = last_day_of_current_month.day

                # Calculate interest for the month
                if (
                    current_date.year == start_date.year
                    and current_date.month == start_date.month
                ):
                    days_invested = (
                        last_day_of_current_month - start_date
                    ).days + 1
                    interest = (
                        balance
                        * monthly_rate
                        * (days_invested / total_days_in_month)
                    )
                elif (
                    current_date.year == end_date.year
                    and current_date.month == end_date.month
                ):
                    days_invested = (
                        end_date - get_first_day_of_month(current_date)
                    ).days
                    interest = (
                        balance
                        * monthly_rate
                        * (days_invested / total_days_in_month)
                    )
                else:
                    interest = balance * monthly_rate

                balance += interest
                total_interest += interest

                # Contribution logic
                contribution = 0.0
                contribution_date = current_date.replace(day=23)

                is_contribution_month = (
                    start_date <= contribution_date <= end_date
                    and (
                        current_date.year != start_date.year
                        or current_date.month != start_date.month
                        or start_date.day <= 23
                    )
                    and (
                        current_date.year != end_date.year
                        or current_date.month != end_date.month
                        or end_date.day >= 23
                    )
                )

                if is_contribution_month:
                    contribution = monthly_contribution
                    balance += contribution

                # Record data for the month
                data.append(
                    {
                        "Month": current_date.strftime("%Y-%m"),
                        "Interest Earned (€)": format_currency(interest),
                        "Contribution (€)": format_currency(contribution),
                        "End Balance (€)": format_currency(balance),
                    }
                )

                # Move to the next month safely
                current_date = get_first_day_of_month(current_date) + relativedelta(
                    months=1
                )

            # Update DataTable
            breakdown_table.rows = []
            for row in data:
                breakdown_table.rows.append(
                    DataRow(
                        cells=[
                            DataCell(Text(row["Month"])),
                            DataCell(Text(row["Interest Earned (€)"])),
                            DataCell(Text(row["Contribution (€)"])),
                            DataCell(Text(row["End Balance (€)"])),
                        ]
                    )
                )

            # Update output texts
            total_interest_text.value = (
                f"Total Interest Earned: {format_currency(total_interest)}"
            )
            final_balance_text.value = (
                f"Final Savings Amount: {format_currency(balance)}"
            )

            # Refresh the page to show updates
            page.update()

        except ValueError as ve:
            # Show a Snackbar with the error message
            page.snack_bar = SnackBar(Text(str(ve)), bgcolor="red")
            page.snack_bar.open = True
            page.update()
        except TypeError as te:
            page.snack_bar = SnackBar(
                Text(f"Type error: {str(te)}"), bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            page.snack_bar = SnackBar(
                Text(f"An unexpected error occurred: {str(e)}"), bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()

    # Arrange controls in the UI
    page.add(
        Container(
            content=Column(
                [
                    Text(
                        "📈 Compound Interest Calculator",
                        size=24,
                        weight="bold",
                        text_align="center",
                    ),
                    Row(
                        [
                            Column(
                                [
                                    start_date_field,
                                    end_date_field,
                                    initial_amount_input,
                                    annual_interest_input,
                                    monthly_contribution_input,
                                    calculate_button,
                                ],
                                spacing=10,
                            ),
                            Column(
                                [
                                    total_interest_text,
                                    final_balance_text,
                                ],
                                spacing=10,
                                alignment="start",
                            ),
                        ],
                        alignment="spaceEvenly",
                        spacing=50,
                    ),
                    Text(
                        "📊 Monthly Breakdown",
                        size=20,
                        weight="bold",
                        text_align="center",
                    ),
                    breakdown_table,
                ],
                alignment="start",
                spacing=20,
            ),
            padding=padding.all(20),
        )
    )


# Launch the Flet app
if __name__ == "__main__":
    flet.app(target=main)
