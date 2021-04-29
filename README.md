<h1 align="center">
  Crypto Price Alert 🔔
</h1>
<p>
The script uses the Coingecko API to get real-time prices and send you an email,
if you the price of an asset gets above/below your goal.
</p>

## Getting started

1.  **Prerequisites**

    Before you start, you should have Python 3 with Pip installed.

    Then set up a virtual environment and install the required packages inside the project.

    ```shell
    pip install -r requirements.txt
    ```

2.  **Configuration**

    Now you can configure the mail server and assets you want to keep an eye on. _.env_ file.
    There already is a .env.example file, which you can rename and use.
    You need to set the time interval in seconds in which the script is getting executed.
    It is also possible to define a list of assets you are interested in.
    The script will check if any of the assets is currently trending at the coingecko search chart.

    ```shell
    TIME_INTERVAL=600
    WATCHED_ASSETS=['BTC', 'ETH', '...']
    ```

3.  **Start the script.**

    You can start the script by running the main file and follow the instructions in the console.
    Enjoy experimenting with the script.

    ```shell
    python main.py
    ```
