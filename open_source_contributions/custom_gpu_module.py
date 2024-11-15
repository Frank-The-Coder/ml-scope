import torch
from config.device_config import device

def optimize_batch_processing(data, batch_size=32):
    """
    Optimizes batch processing by leveraging GPU acceleration if available.
    """
    data = torch.tensor(data).to(device)

    batched_data = torch.split(data, batch_size)
    results = []
    for batch in batched_data:
        # Simulate processing
        results.append(batch.mean(dim=0).cpu().numpy())

    return results
