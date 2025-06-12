def get_model_params(model_path, framework="generic"):
    try:
        if framework == "pytorch":
            import torch
            model = torch.load(model_path)
            return sum(p.numel() for p in model.parameters())
        elif framework == "tensorflow":
            import tensorflow as tf
            model = tf.keras.models.load_model(model_path)
            return model.count_params()
        else:
            return None
    except Exception as e:
        print("Cannot parse model params:", e)
        return None
