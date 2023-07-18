# Dependencies pip install tabulate

import argparse
import subprocess
from tabulate import tabulate

def run_kubectl_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return stdout.decode("utf-8").strip()

def get_kubectl_output(command):
    return run_kubectl_command(f"kubectl {command}")

def organize_output(output):
    lines = output.split("\n")
    headers = lines[0].split()
    data = [line.split() for line in lines[1:] if line.strip()]
    return headers, data

def main(namespace):
    pods_output = get_kubectl_output(f"get pods -n {namespace} --show-labels")
    pods_headers, pods_data = organize_output(pods_output)

    services_output = get_kubectl_output(f"get services -n {namespace} --show-labels")
    services_headers, services_data = organize_output(services_output)

    endpoints_output = get_kubectl_output(f"get endpoints -n {namespace} --show-labels")
    endpoints_headers, endpoints_data = organize_output(endpoints_output)

    print("PODS:")
    print(tabulate(pods_data, headers=pods_headers, tablefmt="grid"))

    print("\nSERVICES:")
    print(tabulate(services_data, headers=services_headers, tablefmt="grid"))

    print("\nENDPOINTS:")
    print(tabulate(endpoints_data, headers=endpoints_headers, tablefmt="grid"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Kubernetes resources in a namespace.")
    parser.add_argument("-n", "--namespace", required=True, help="The namespace to process.")
    args = parser.parse_args()

    main(args.namespace)

