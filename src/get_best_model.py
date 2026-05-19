import mlflow
from mlflow.tracking import MlflowClient

def get_best_model():
    client = MlflowClient()
    experiment_name = "house_price_prediction"

    experiment = client.get_experiment_by_name(experiment_name)
    experiment_id = experiment.experiment_id

    runs = client.search_runs(experiment_id, order_by=["metrics.mae ASC"], max_results=1)

    if not runs:
        print("No runs found for the experiment.")
        return None 
    best_run = runs[0]
    best_run_id = best_run.info.run_id
    best_mae = best_run.data.metrics['mae']

    print(f"Best Run ID: {best_run_id}")
    print(f"Best MAE: {best_mae}")
    print(f"Model URI: runs:/{best_run_id}/model")

    return best_run_id
if __name__ == "__main__":
    get_best_model()
