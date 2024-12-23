# Compound Interest Calculator

A Python application to calculate and visualize compound interest over time with monthly contributions. The application
provides a detailed monthly breakdown of savings growth.

## Features

- Input fields for:
  - Start and end dates
  - Initial investment amount
  - Annual interest rate
  - Monthly contribution amount
- Calculate and display:
  - Total interest earned
  - Final balance
  - Monthly breakdown table showing:
    - Month/Year
    - Interest earned
    - Contribution amount
    - End balance

## Requirements

- Python 3.13.1
- Flet framework
- `python-dateutil` library

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/neowim/compound-interest-calculator.git
    cd compound-interest-calculator
    ```

2. Create and activate a virtual environment:

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

    ```sh
    python main.py
    ```

2. Open your web browser and navigate to the provided local URL to use the application.

## Project Structure

- [main.py](https://github.com/neowim/compound-interest-calculator/blob/main/main.py): Main application file with the
    compound interest calculator implementation.
- [requirements.txt](https://github.com/neowim/compound-interest-calculator/blob/main/requirements.txt): List of
    dependencies required for the project.
- [.envrc](https://github.com/neowim/compound-interest-calculator/blob/main/.envrc): Environment configuration for the
    project.
- [functional_requirements.txt](https://github.com/neowim/compound-interest-calculator/blob/main/functional_requirements.txt):
    Functional requirements documentation.
- [settings.json](https://github.com/neowim/compound-interest-calculator/blob/main/settings.json): VS Code settings
    for the project.
- [changelog.txt](https://github.com/neowim/compound-interest-calculator/blob/main/changelog.txt): Project changelog
    documenting changes and updates.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [Flet](https://flet.dev/) - GUI framework used in this project.
- [python-dateutil](https://dateutil.readthedocs.io/en/stable/) - Library for date handling.

## Contact

For any questions or suggestions, please open an issue or contact the repository owner.
