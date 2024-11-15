# ML-Scope: A Real-Time Machine Learning Pipeline for Forecasting and Reinforcement Learning

## Overview

ML-Scope is a comprehensive project designed to simulate a scalable real-time machine learning pipeline that integrates **forecasting models**, **reinforcement learning (RL)**, and robust **queue management**. The project emphasizes **hyperparameter experimentation**, **resilience testing**, and **modular scalability**, preparing for real-world applications in AI and ML engineering roles.

Through this project, critical skills such as **real-time queue management**, **hardware-aware optimizations**, and **reinforcement learning integration** are demonstrated and addressed.

---

## Key Features

1. **Real-Time Prediction Queue**:

   - A shared prediction queue facilitates inter-process communication between forecasting and RL modules.
   - Queue operations include logging for enqueue and dequeue events to track latency and overflow scenarios.

2. **Forecasting Model with Hardware Awareness**:

   - LSTM-based forecasting model with automatic hardware detection (CPU/GPU).
   - Dynamic quantization optimizes performance for CPU-based inference when GPUs are unavailable.

3. **Reinforcement Learning Integration**:

   - Q-learning agent processes real-time predictions for adaptive decision-making.
   - Logs all actions, rewards, and cumulative rewards for performance analysis.

4. **Experimental Pipeline**:

   - Automates hyperparameter optimization across learning rate, exploration rate, and discount factor.
   - Resilience testing simulates high-load scenarios to validate queue and model performance.

5. **Scalability and Modular Design**:

   - Modular structure for easy extensions, such as adding forecasting models or integrating with custom accelerators.

6. **Comprehensive Logging**:
   - Centralized logging tracks queue operations, RL training, and forecasting activities.

---

## Recent Enhancements

### **1. Advanced Logging System**

- **Queue Monitoring**: Logs every enqueue and dequeue operation with timestamps and latencies in `logs/queue_processing.log`.
- **RL-Specific Logs**: Logs RL actions, rewards, and cumulative rewards in `logs/rl_training.log`.
- **Custom Logging Configuration**: Centralized in `config/logging_config.py` to manage different logging streams independently.

### **2. GPU and CPU Optimization**

- Forecasting and RL models now detect hardware capabilities using `config/device_config.py`.
- Implements **torch quantization** to dynamically optimize for CPU when GPUs are unavailable.
  ```python
  model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
  ```

### **3. Automated Hyperparameter Tuning**

- `experimental_pipeline/pipeline.py` automates testing of different RL configurations, including:
  - Learning Rate: 0.01, 0.1, 0.5
  - Exploration Rate: 1.0, 0.8, 0.5
  - Discount Factor: 0.9, 0.95, 0.99
- Results are logged with final rewards for analysis and selection of optimal parameters.

### **4. Resilience Testing**

- `experimental_pipeline/resilience_testing.py` rapidly generates predictions to test queue stability under high load.
- Ensures system robustness by logging enqueue delays and analyzing performance.

### **5. Modular Extensions**

- Developed `open_source_contributions/custom_gpu_module.py` for integrating custom GPU optimizations or AI accelerators.
- Logs integration steps in `docs/integration_notes.md` to assist future contributors.

---

## Technical Details

### **Real-Time Prediction Queue**

- **File**: `forecasting_model/queue_server.py`
- Implements a **shared queue** with Python's `multiprocessing.managers.BaseManager`.
- Logs queue operations in real time, including overflow handling:
  ```python
  if prediction_queue.full():
      prediction_queue.get()  # Remove the oldest prediction
  log_enqueue(prediction_queue, prediction)
  ```

### **Forecasting Model**

- **File**: `forecasting_model/forecast_training.py`
- LSTM-based forecasting with quantization for CPU optimization:
  ```python
  model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
  ```
- Generates predictions and enqueues them into the shared queue for downstream processing.

### **Reinforcement Learning Agent**

- **Files**:
  - `forecasting_model/rl_training.py`: RL training script with real-time prediction consumption.
  - `forecasting_model/rl_utils.py`: Helper functions for Q-learning and state management.
- Tracks and logs all RL actions and rewards in `logs/rl_training.log`:
  ```python
  rl_logger.info(f"Action={action}, Reward={reward}, Cumulative Reward={total_reward}")
  ```

### **Experimental Pipeline**

- **File**: `experimental_pipeline/pipeline.py`
- Tests hyperparameter combinations, logging rewards for each configuration.
- Automatically terminates RL training when the prediction queue is empty during testing.

### **Resilience Testing**

- **File**: `experimental_pipeline/resilience_testing.py`
- Rapidly enqueues predictions to simulate high-traffic conditions.
- Logs all enqueue/dequeue operations and performance metrics for debugging.

For a complete breakdown of the technical structure, including key files and their functionalities, see the [Architecture Documentation](docs/architecture.md).

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
├── config/
│   ├── logging_config.py     # Modular logging setup
│   ├── device_config.py      # Hardware detection and configuration
│   └── __init__.py
├── experimental_pipeline/
│   ├── pipeline.py           # Experimental pipeline for hyperparameter tuning
│   ├── resilience_testing.py # Resilience testing for high-load scenarios
│   └── __init__.py
├── open_source_contributions/
│   ├── custom_gpu_module.py  # Custom GPU optimization plugin
│   └── integration_notes.md  # Notes for integrating external contributions
├── docs/
│   ├── README.md             # Main project overview
│   ├── architecture.md       # System architecture documentation
│   ├── setup_instructions.md # Local setup instructions
│   ├── integration_notes.md  # Integration documentation
│   └── api_documentation.md  # API details
├── logs/                     # Log files for queue operations and training
├── tests/                    # Automated tests for resilience and integration
├── requirements.txt          # Project dependencies
└── README.md                 # Project overview
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- A virtual environment (recommended)

1. **Setup**:

   - Install dependencies:

     ```bash
     pip install -r requirements.txt
     ```

   - Start the queue server:
     ```bash
     python forecasting_model/queue_server.py
     ```

2. **Run Forecasting Model**:

   - Generate predictions:
     ```bash
     python forecasting_model/forecast_training.py
     ```

3. **Run RL Training**:

   - Start RL agent:
     ```bash
     python forecasting_model/rl_training.py
     ```

4. **Run Experiments**:
   - Launch experimental pipeline:
     ```bash
     python experimental_pipeline/pipeline.py
     ```

---

## Contributing

We welcome contributions to ML-Scope! If you’d like to contribute, please read the [Contributing Guidelines](CONTRIBUTING.md) to get started.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

Thank you to all contributors and collaborators who helped build ML-Scope into a robust real-time RL pipeline.
