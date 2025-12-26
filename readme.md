# 📂 Airflow Local DAG Development

This repository serves as a template for developing Airflow DAGs locally. It utilizes a **remote platform configuration** to deploy a full Airflow 3 stack on Minikube without requiring local Docker builds.

## 📋 Prerequisites

Before running this project, ensure the following tools are installed and configured:

* **Docker Runtime**: [Docker Desktop](https://www.docker.com/products/docker-desktop/) or [Colima](https://github.com/abiosoft/colima) (recommended for macOS).
* **Minikube**: A local Kubernetes cluster.
* **Skaffold**: Version `v2.17.0` or higher.
* **Helm**: Version `v4.0.4` or higher.
* **Git**: Required to fetch the remote Skaffold dependencies.

---

## 🚀 Getting Started

### 1. Start the File Bridge (The Mount)

To see your local DAGs inside the Airflow cluster, you must mount your project directory into the Minikube VM. This command must remain running in a dedicated terminal window.

```bash
# Maps your current folder to /app inside Minikube with Airflow permissions
minikube mount .:/app

```

### 2. Execute Skaffold

In a new terminal window, start the deployment. Skaffold will fetch the remote configuration from GitHub and deploy the stack to your local cluster.

```bash
skaffold dev

```

### 3. Access Airflow

Once the pods are `Running` (verify via `k9s` or `kubectl get pods -n airflow`), you can access the UI. Skaffold is configured to automatically port-forward the API Server.

* **URL**: [http://localhost:8080](http://localhost:8080)
* **Default Credentials**: `admin` / `admin`

---

## 🛠 Project Structure

* **`skaffold.yaml`**: The local configuration that imports the remote `skaffold-helm-minikube-remote` repository.
* **`dags/`**: Place your `.py` DAG files here. They are live-mounted into the cluster.
* **`.gitignore`**: Pre-configured to ignore local environment files, caches, and Minikube state.

---

## ❓ FAQ & Troubleshooting

### Why are my DAGs not appearing in the UI?

1. **Check the Mount**: Ensure the `minikube mount` command is still running. If it was interrupted, restart it and then restart the Airflow pods.
2. **Parsing Delay**: Airflow 3 can take up to 60 seconds to parse new files. Check the `airflow-dag-processor` logs for errors.

### How do I add a new Python library?

This is a **"No-Build"** workflow. To add a new library:

* **Temporary**: `kubectl exec` into the `scheduler` or `dag-processor` and run `pip install <package>`.
* **Permanent**: Request an update to the base image in the `platform.azurecr.io/udo/airflow` registry.

### My pods are stuck in `Init:0/1`. What do I do?

The pods are waiting for the database migration job to complete. If it hangs:

1. Run `kubectl get jobs -n airflow` to see the status.
2. Check the logs of the `airflow-run-airflow-migrations` pod.

### Can I change the Airflow configuration?

Yes. You can add a `values-local.yaml` file to your project and reference it in your `skaffold.yaml` to override any default settings (e.g., changing memory limits or enabling/disabling specific components).