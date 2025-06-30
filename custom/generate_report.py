"""
Utility script to generate a load test report from Locust results.

This script connects to a running Locust instance, retrieves test statistics,
and generates a report with analysis of the results.

Usage:
    python generate_report.py --host=localhost --port=8089 --output=report.html
"""

import os
import sys
import json
import argparse
import requests
import datetime
from pathlib import Path

# Add the parent directory to sys.path to allow importing config
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))

from app.core.locust_load_test.custom.config import (
    LOCUST_MASTER_HOST,
    LOCUST_MASTER_PORT,
)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate load test report from Locust")
    
    parser.add_argument("--host", type=str, default=LOCUST_MASTER_HOST, 
                        help=f"Locust master host (default: {LOCUST_MASTER_HOST})")
    parser.add_argument("--port", type=int, default=LOCUST_MASTER_PORT, 
                        help=f"Locust master port (default: {LOCUST_MASTER_PORT})")
    parser.add_argument("--output", type=str, default="load_test_report.html", 
                        help="Output file for the report (default: load_test_report.html)")
    
    return parser.parse_args()


def get_locust_stats(host, port):
    """Retrieve statistics from Locust"""
    endpoints = {
        "stats": f"http://{host}:{port}/stats/requests",
        "errors": f"http://{host}:{port}/stats/failures",
        "exceptions": f"http://{host}:{port}/exceptions",
        "workers": f"http://{host}:{port}/workers",
    }
    
    results = {}
    
    for name, url in endpoints.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                results[name] = response.json()
            else:
                print(f"Warning: Could not retrieve {name}. Status code: {response.status_code}")
                results[name] = {"error": f"Status code: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving {name}: {e}")
            results[name] = {"error": str(e)}
    
    return results


def generate_html_report(stats, output_file):
    """Generate an HTML report from the statistics"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Extract key statistics
    total_stats = stats.get("stats", {}).get("stats", [])
    errors = stats.get("errors", {}).get("failures", [])
    exceptions = stats.get("exceptions", {}).get("exceptions", [])
    workers = stats.get("workers", {}).get("workers", [])
    
    # Create HTML content
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FastAPI Load Test Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 20px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .summary {{
            background-color: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .good {{
            color: green;
        }}
        .warning {{
            color: orange;
        }}
        .critical {{
            color: red;
        }}
    </style>
</head>
<body>
    <h1>FastAPI Load Test Report</h1>
    <p>Generated on: {now}</p>
    
    <div class="summary">
        <h2>Summary</h2>
"""
    
    # Add summary statistics
    if total_stats:
        total_requests = sum(stat.get("num_requests", 0) for stat in total_stats)
        total_failures = sum(stat.get("num_failures", 0) for stat in total_stats)
        failure_rate = (total_failures / total_requests * 100) if total_requests > 0 else 0
        
        # Calculate average response time across all endpoints
        avg_response_times = [stat.get("avg_response_time", 0) for stat in total_stats if stat.get("avg_response_time")]
        avg_response_time = sum(avg_response_times) / len(avg_response_times) if avg_response_times else 0
        
        # Find max response time
        max_response_time = max([stat.get("max_response_time", 0) for stat in total_stats]) if total_stats else 0
        
        # Determine status class based on metrics
        failure_class = "good" if failure_rate < 1 else "warning" if failure_rate < 5 else "critical"
        response_class = "good" if avg_response_time < 200 else "warning" if avg_response_time < 500 else "critical"
        
        html += f"""
        <p><strong>Total Requests:</strong> {total_requests}</p>
        <p><strong>Total Failures:</strong> {total_failures}</p>
        <p><strong>Failure Rate:</strong> <span class="{failure_class}">{failure_rate:.2f}%</span></p>
        <p><strong>Average Response Time:</strong> <span class="{response_class}">{avg_response_time:.2f} ms</span></p>
        <p><strong>Maximum Response Time:</strong> {max_response_time:.2f} ms</p>
        <p><strong>Active Workers:</strong> {len(workers)}</p>
"""
    else:
        html += "<p>No statistics available</p>"
    
    html += """
    </div>
    
    <h2>Endpoint Performance</h2>
    <table>
        <tr>
            <th>Endpoint</th>
            <th>Requests</th>
            <th>Failures</th>
            <th>Median (ms)</th>
            <th>Average (ms)</th>
            <th>Min (ms)</th>
            <th>Max (ms)</th>
            <th>RPS</th>
            <th>Failure %</th>
        </tr>
"""
    
    # Add endpoint statistics
    for stat in total_stats:
        name = stat.get("name", "Unknown")
        num_requests = stat.get("num_requests", 0)
        num_failures = stat.get("num_failures", 0)
        median_response_time = stat.get("median_response_time", 0)
        avg_response_time = stat.get("avg_response_time", 0)
        min_response_time = stat.get("min_response_time", 0)
        max_response_time = stat.get("max_response_time", 0)
        current_rps = stat.get("current_rps", 0)
        
        failure_percent = (num_failures / num_requests * 100) if num_requests > 0 else 0
        failure_class = "good" if failure_percent < 1 else "warning" if failure_percent < 5 else "critical"
        response_class = "good" if avg_response_time < 200 else "warning" if avg_response_time < 500 else "critical"
        
        html += f"""
        <tr>
            <td>{name}</td>
            <td>{num_requests}</td>
            <td>{num_failures}</td>
            <td>{median_response_time:.2f}</td>
            <td class="{response_class}">{avg_response_time:.2f}</td>
            <td>{min_response_time:.2f}</td>
            <td>{max_response_time:.2f}</td>
            <td>{current_rps:.2f}</td>
            <td class="{failure_class}">{failure_percent:.2f}%</td>
        </tr>
"""
    
    html += """
    </table>
    
    <h2>Errors</h2>
"""
    
    if errors:
        html += """
    <table>
        <tr>
            <th>Endpoint</th>
            <th>Error</th>
            <th>Occurrences</th>
        </tr>
"""
        for error in errors:
            html += f"""
        <tr>
            <td>{error.get("name", "Unknown")}</td>
            <td>{error.get("error", "Unknown error")}</td>
            <td>{error.get("occurrences", 0)}</td>
        </tr>
"""
        html += """
    </table>
"""
    else:
        html += "<p>No errors recorded</p>"
    
    html += """
    <h2>Exceptions</h2>
"""
    
    if exceptions:
        html += """
    <table>
        <tr>
            <th>Count</th>
            <th>Exception</th>
            <th>Traceback</th>
        </tr>
"""
        for exception in exceptions:
            html += f"""
        <tr>
            <td>{exception.get("count", 0)}</td>
            <td>{exception.get("exc_type", "Unknown")}: {exception.get("exc_message", "")}</td>
            <td><pre>{exception.get("traceback", "")}</pre></td>
        </tr>
"""
        html += """
    </table>
"""
    else:
        html += "<p>No exceptions recorded</p>"
    
    # Add recommendations section
    html += """
    <h2>Recommendations</h2>
"""
    
    recommendations = []
    
    # Add recommendations based on results
    if total_stats:
        if failure_rate > 5:
            recommendations.append("High failure rate detected. Investigate the errors and exceptions listed above.")
        
        if avg_response_time > 500:
            recommendations.append("Average response time is high. Consider optimizing database queries, adding caching, or scaling the application.")
        
        slow_endpoints = [stat for stat in total_stats if stat.get("avg_response_time", 0) > 500]
        if slow_endpoints:
            slow_endpoint_names = ", ".join([stat.get("name", "Unknown") for stat in slow_endpoints])
            recommendations.append(f"Slow endpoints detected: {slow_endpoint_names}. These endpoints need optimization.")
        
        if len(workers) < 2 and total_requests > 1000:
            recommendations.append("For higher load testing, consider running in distributed mode with more worker nodes.")
    
    if not recommendations:
        recommendations.append("The application is performing well under the current load.")
    
    for recommendation in recommendations:
        html += f"<p>• {recommendation}</p>"
    
    html += """
    <h2>Raw Data</h2>
    <pre style="background-color: #f5f5f5; padding: 10px; overflow: auto;">
"""
    
    # Add raw JSON data
    html += json.dumps(stats, indent=2)
    
    html += """
    </pre>
    
    <footer>
        <p>Generated by FastAPI Load Test Report Generator</p>
    </footer>
</body>
</html>
"""
    
    # Write the HTML report to file
    with open(output_file, "w") as f:
        f.write(html)
    
    print(f"Report generated: {output_file}")


def main():
    args = parse_arguments()
    
    print(f"Connecting to Locust at {args.host}:{args.port}...")
    stats = get_locust_stats(args.host, args.port)
    
    print(f"Generating report to {args.output}...")
    generate_html_report(stats, args.output)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
