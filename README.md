# Asyncio-Scheduler

This project provides an asyncio-based non-blocking scheduler that accepts a cron expression and additional parameters for minutes, hours, date, week, date, seconds, and interval. It can be used as a decorator over any method, enabling it to work as a Python asynchronous scheduler.

## Installation

To use this scheduler, follow the steps below:

1. Clone the repository:

   bash
   git clone [[https://github.com/example/repository.git](https://github.com/Hithhuuu/asynio-scheduler.git)](https://github.com/Hithhuuu/asyncio-scheduler.git)
   

2. Install the required dependencies:

   bash
   pip install -r requirements.txt
   

## Usage

1. Import the necessary modules:

   python
   import asyncio
   import croniter
   from scheduler import scheduler_cron
   

2. Create an instance of the `scheduler` method:

   python
   scheduler = scheduler_cron()
   

3. Define a function or method that you want to schedule:

   python
   async def my_task():
       # Your code here
       pass
   

4. Decorate your function or method with the `@scheduler_cron` decorator:

   python
   @scheduler_cron(cron_expression, minutes=0, hours=0, date=None, week=None, seconds=0, interval=None)
   async def my_task():
       # Your code here
       pass
   

   Replace the `cron_expression` parameter with your desired cron expression. The additional parameters (`minutes`, `hours`, `date`, `week`, `seconds`, and `interval`) provide flexibility in scheduling.

5. Start the scheduler:

   python
   asyncio.run(file.py)
   

   This will run the scheduler and execute your scheduled task at the specified intervals based on the cron expression and additional parameters.

## Example

Here's an example that demonstrates the usage of the asyncio-based non-blocking scheduler:

python
import asyncio
from scheduler import scheduler_cron

async def my_task():
    print("Task executed!")

scheduler = scheduler_cron()

# Schedule the task to run every minute
@scheduler_cron("* * * * *")
async def my_task():
    print("Task executed!")



In this example, the task is scheduled to run every minute. The scheduler runs for 10 seconds, executing the task at the specified interval.

## Contributing

Contributions are welcome! If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b my-new-feature`.
3. Make your changes and commit them: `git commit -am 'Add new feature'`.
4. Push to the branch: `git push origin my-new-feature`.
5. Submit a pull request explaining your changes.

## License

This project is licensed under the [MIT License](LICENSE).
