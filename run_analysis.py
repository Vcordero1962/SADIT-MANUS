from src.sadit.inference.bayesian import SaditBayesianEngine

print("Initializing SADIT Learning Core...")
engine = SaditBayesianEngine()
print("Starting Multimodal Training...")
engine.train_from_multimodal()
