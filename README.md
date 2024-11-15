# ML-Scope: A Real-Time Reinforcement Learning Pipeline with Queue Management

## Overview

ML-Scope is a reinforcement learning (RL) project designed to simulate real-time decision-making using a shared prediction queue. This project integrates a real-time forecasting model, a reinforcement learning agent, and robust queue handling mechanisms. It emphasizes resilience testing, hyperparameter experimentation, and scalability for real-time systems.

This project also addresses critical skill gaps, such as:

- Real-time queue management
- Reinforcement learning integration
- Resilience testing under high-load conditions
- Experimentation with hyperparameter tuning

## Key Features

1. **Real-Time Prediction Queue**:

   - Forecasting model generates predictions and enqueues them for real-time decision-making.
   - Queue size is capped at 100, ensuring efficient memory usage and preventing overflow.

2. **Reinforcement Learning Integration**:

   - The RL agent uses predictions from the queue to make real-time decisions.
   - A Q-learning algorithm trains the agent to optimize decisions based on incoming predictions.

3. **Resilience Testing**:

   - High-load scenarios are simulated to test queue stability and system robustness.
   - Custom logging tracks queue performance, including enqueue and dequeue delays.

4. **Experimentation Pipeline**:

   - An experimental pipeline tests various RL hyperparameters (learning rate, exploration rate, discount factor).
   - Results are logged and analyzed for performance optimization.

5. **Scalable and Modular Design**:
   - Modular structure ensures separation of concerns (e.g., prediction generation, RL training, resilience testing).
   - Supports future extensions for additional forecasting models or RL agents.

---

## Technical Details

### 1. Real-Time Prediction Queue

- **Implementation**: `forecasting_model/queue_server.py`
- **Description**:
  - A shared queue is managed using Python’s `multiprocessing.managers.BaseManager`.
  - Forecasting models enqueue predictions, and the RL agent dequeues them in real-time.
  - Queue operations include logging for enqueue and dequeue timestamps to monitor delays.
- **Key Features**:
  - Maximum queue size of 100 to prevent overflow.
  - Overwrite logic to replace oldest predictions when the queue is full.

### 2. Forecasting Model

- **Implementation**: `forecasting_model/forecast_training.py`
- **Description**:
  - Generates predictions using an LSTM-based model.
  - Predictions are enqueued into the shared queue for processing by the RL agent.
  - Handles queue overflow gracefully, logging warnings when predictions are skipped.
- **Key Features**:
  - Real-time prediction generation at configurable intervals.
  - Scalable LSTM architecture for handling larger datasets.

### 3. Reinforcement Learning Agent

- **Implementation**: `forecasting_model/rl_training.py`, `forecasting_model/rl_utils.py`
- **Description**:
  - The RL agent uses a custom Q-learning implementation to optimize decisions based on predictions dequeued from the shared queue.
  - Actions are chosen dynamically using an exploration-exploitation strategy, with rewards derived from predictions.
- **Key Features**:
  - Real-time decision-making integrated with the prediction queue.
  - Action-based reward scaling to guide learning.
  - Supports hyperparameter tuning for learning rate, exploration rate, and discount factor.

### 4. Resilience Testing

- **Implementation**: `experimental_pipeline/resilience_testing.py`
- **Description**:
  - Simulates high-load scenarios by rapidly enqueuing predictions into the shared queue.
  - Tests queue handling, including logging delays and monitoring performance under stress.
- **Key Features**:
  - Customizable number of predictions and enqueue delay.
  - Logs detailed queue metrics for debugging and analysis.

### 5. Experimental Pipeline

- **Implementation**: `experimental_pipeline/pipeline.py`
- **Description**:
  - Automates hyperparameter tuning for the RL agent.
  - Runs multiple experiments with different configurations of learning rate, exploration rate, and discount factor.
  - Automatically stops RL training when all predictions are processed.
- **Key Features**:
  - Parallel monitoring of queue state to trigger training termination.
  - Logs results for each hyperparameter configuration.

---

## Project Structure

```
ml-scope/
├── forecasting_model/
│   ├── rl_training.py        # RL training with queue integration
│   ├── rl_utils.py           # RL environment and Q-learning implementation
│   ├── forecast_training.py  # Forecasting model for prediction generation
│   ├── queue_server.py       # Shared queue implementation
│   ├── queue_monitor.py      # Logs queue enqueue and dequeue operations
│   └── __init__.py
├── experimental_pipeline/
│   ├── pipeline.py           # Experimental pipeline for hyperparameter tuning
│   ├── resilience_testing.py # Resilience testing for high-load scenarios
│   └── __init__.py
├── logs/                     # Log files for queue operations and training
├── tests/                    # Automated tests for resilience and integration
├── docs/                     # Documentation for architecture and setup
├── requirements.txt          # Project dependencies
└── README.md                 # Project overview and details
```

---

## Getting Started

1. **Setup**:

   - Install dependencies: `pip install -r requirements.txt`.
   - Start the queue server: `python forecasting_model/queue_server.py`.

2. **Run Forecasting Model**:

   - Generate predictions: `python forecasting_model/forecast_training.py`.
   - Resilience Testing: `python experimental_pipeline/resilience_testing.py`.

3. **Run RL Training**:

   - Start RL agent: `python forecasting_model/rl_training.py`.

4. **Run Experiments**:
   - Launch experimental pipeline: `python experimental_pipeline/pipeline.py`.

---

## Goals

This project addresses the following objectives:

- Demonstrating real-time queue handling and decision-making.
- Building expertise in reinforcement learning with dynamic data.
- Testing system resilience under high-load conditions.
- Exploring hyperparameter optimization for RL agents.
