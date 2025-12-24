import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
# === ADDED: Graphing Functions for Quantitative Analysis ===



import cartopy.crs as ccrs
import cartopy.feature as cfeature
import time
import random
from concurrent.futures import ThreadPoolExecutor

# ==== CONFIG ====
# Use the exact URL without any query parameters
CDN_AVATAR_URL = 'https://cdn.discordapp.com/avatars/1368314962623201352/1379ceb959c105e6f137e75b0697ad59.png?size=1024'

# Add more geographically diverse proxies - these are just examples, replace with working proxies
# Try to include proxies from different countries/regions for better geographical distribution
PROXIES = [
    None,
    'http://50.223.246.237:80', 'http://50.174.7.159:80', 'http://50.207.199.87:80', 'http://32.223.6.94:80',
    'http://50.207.199.80:80', 'http://50.207.199.83:80', 'http://50.174.7.153:80', 'http://50.202.75.26:80',
    'http://50.239.72.18:80', 'http://50.175.212.66:80', 'http://50.217.226.47:80', 'http://50.239.72.16:80',
    'http://50.239.72.19:80', 'http://50.217.226.40:80', 'http://50.221.74.130:80', 'http://50.175.212.74:80',
    'http://50.207.199.82:80', 'http://50.174.7.152:80', 'http://50.122.86.118:80', 'http://66.191.31.158:80',
    'http://89.187.185.88:3128', 'http://23.247.136.254:80', 'http://34.102.48.89:8080', 'http://54.174.151.201:80',
    'http://40.76.69.94:8080', 'http://155.94.128.59:10809', 'http://50.217.226.43:80', 'http://50.239.72.17:80',
    'http://50.174.7.157:80', 'http://50.217.226.44:80', 'http://50.174.7.158:80', 'http://50.217.226.42:80',
    'http://50.174.7.155:80', 'http://50.174.7.162:80', 'http://162.223.90.150:80', 'http://50.221.230.186:80',
    'http://198.74.51.79:8888', 'http://192.73.244.36:80', 'http://198.49.68.80:80', 'http://50.217.226.41:80',
    'http://50.207.199.86:80', 'http://68.185.57.66:80', 'http://50.231.104.58:80', 'http://50.174.7.156:80',
    'http://50.207.199.81:80', 'http://47.252.18.37:6379', 'http://47.252.11.233:8443', 'http://23.82.137.161:80',
    'http://159.65.245.255:80', 'http://23.247.136.248:80'
    # Will add more proxies if necessary
]

POPS_LAT_LON = {
    'IAD': (39.0, -77.0),       # Ashburn, VA
    'ATL': (33.6407, -84.4277), # Atlanta, GA
    'BOS': (42.3656, -71.0096), # Boston, MA
    'ORD': (41.9742, -87.9073), # Chicago, IL
    'DFW': (32.8998, -97.0403), # Dallas, TX
    'DEN': (39.8561, -104.6737),# Denver, CO
    'IAH': (29.9902, -95.3368), # Houston, TX
    'LAS': (36.085, -115.1511), # Las Vegas, NV
    'LAX': (33.9416, -118.4085),# Los Angeles, CA
    'MIA': (25.7959, -80.2870), # Miami, FL
    'MSP': (44.8820, -93.2218), # Minneapolis, MN
    'JFK': (40.6413, -73.7781), # New York City, NY
    'EWR': (40.6895, -74.1745), # Newark, NJ
    'PHX': (33.4342, -112.0116),# Phoenix, AZ
    'SFO': (37.6213, -122.3790),# San Francisco, CA
    'SJC': (37.3639, -121.9289),# San Jose, CA
    'SEA': (47.4502, -122.3088),# Seattle, WA
    'STL': (38.7487, -90.3700), # St. Louis, MO
    'TPA': (27.9755, -82.5332), # Tampa, FL
    'SLC': (40.7899, -111.9791),# Salt Lake City, UT
    'MCI': (39.2976, -94.7139), # Kansas City, MO
    'CLE': (41.4117, -81.8498), # Cleveland, OH
    'PDX': (45.5898, -122.5951),# Portland, OR
    'CLT': (35.2140, -80.9431), # Charlotte, NC
    'DTW': (42.2162, -83.3554), # Detroit, MI
    'PHL': (39.8744, -75.2424), # Philadelphia, PA
    'BOM': (19.0896, 72.8656),  # Mumbai
    'MAA': (12.9941, 80.1709),  # Chennai
    'HYD': (17.2403, 78.4294),  # Hyderabad
    'DEL': (28.5562, 77.1000),  # New Delhi
    'CCU': (22.6547, 88.4467),  # Kolkata
    'BLR': (12.9716, 77.5946),   # Bengaluru
    'FRA': (50.0379, 8.5622),  # Frankfurt
    'CDG': (49.0097, 2.5479),  # Paris
    'LHR': (51.4700, -0.4543),  # London
    'AMS': (52.3105, 4.7683),  # Amsterdam
    'NRT': (35.7719, 140.3928),  # Tokyo
    'SYD': (-33.9399, 151.1753),  # Sydney
    'GRU': (-23.4356, -46.4731),  # São Paulo
    'JNB': (-26.1367, 28.2411),  # Johannesburg
    'SIN': (1.3644, 103.9915),  # Singapore
    'HKG': (22.3080, 113.9185)  # Hong Kong
}


def lookup_location(p):
    return POPS_LAT_LON.get(p.upper(), (0, 0))


def validate_proxies(proxy_list):
    working = []
    print("[*] Validating proxies...")

    for proxy in proxy_list:
        if proxy is None:
            working.append(None)
            print("[+] Local (no proxy) is OK")
            continue
        try:
            r = requests.get("https://www.google.com",
                             proxies={"http": proxy, "https": proxy},
                             timeout=5)
            if r.status_code == 200:
                print(f"[+] Proxy works: {proxy}")
                working.append(proxy)
            else:
                print(f"[-] Proxy failed (status {r.status_code}): {proxy}")
        except Exception as e:
            print(f"[-] Proxy failed ({proxy}): {e}")

    return working


def probe_single(proxy=None, attempt=1, session_id=None):
    """Probe a single proxy with optional session ID to track across attempts"""
    try:
        kwargs = {}
        if proxy:
            kwargs['proxies'] = {'http': proxy, 'https': proxy}

        # Create headers that will encourage caching
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            # Don't add Cache-Control headers that might prevent caching
        }

        # Add a session cookie to simulate the same browser across requests
        if session_id:
            headers['Cookie'] = f'session={session_id}'

        # CRITICAL: Use the exact same URL without random parameters to increase cache hit chances
        r = requests.get(CDN_AVATAR_URL, timeout=10, headers=headers, **kwargs)

        ray = r.headers.get('CF-RAY', 'unknown')
        status = r.headers.get('CF-Cache-Status', 'unknown')
        pop = ray.split('-')[1] if '-' in ray else 'unknown'

        # Print diagnostics
        proxy_name = proxy or 'Local'
        print(f"[Probe {attempt}] {proxy_name} - CF-RAY: {ray}, Cache: {status}, PoP: {pop}")

        # Add more info to the result for better analysis
        return {
            'Proxy': proxy_name,
            'PoP': pop,
            'Cache': status,
            'Attempt': attempt,
            'SessionID': session_id,
            'CF-RAY': ray
        }
    except Exception as e:
        print(f"[Error] Proxy {proxy} attempt {attempt}: {e}")
        return None


def probe_sequence(proxy, num_attempts=3):
    """Run a sequence of probes using the same proxy with the same session ID"""
    session_id = f"session_{random.randint(10000, 99999)}"
    results = []

    for attempt in range(1, num_attempts + 1):
        result = probe_single(proxy, attempt, session_id)
        if result:
            results.append(result)
        time.sleep(1)  # Short delay between attempts with the same proxy

    return results


def probe_parallel(proxies, attempts_per_proxy=3):
    """Run probes in parallel for faster execution"""
    all_results = []

    with ThreadPoolExecutor(max_workers=min(10, len(proxies))) as executor:
        future_to_proxy = {executor.submit(probe_sequence, proxy, attempts_per_proxy): proxy for proxy in proxies}
        for future in future_to_proxy:
            try:
                proxy_results = future.result()
                all_results.extend(proxy_results)
            except Exception as e:
                print(f"Error in parallel execution: {e}")

    return all_results


def plot_all_results(df):
    """Plot all results including cache hits and misses with different colors"""
    fig = plt.figure(figsize=(14, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
    ax.gridlines(draw_labels=True)

    # Group by PoP and Cache status for plotting
    grouped = df.groupby(['PoP', 'Cache'])

    # Define colors for different cache statuses
    colors = {
        'HIT': 'green',
        'MISS': 'red',
        'EXPIRED': 'orange',
        'REVALIDATED': 'purple',
        'DYNAMIC': 'blue',
        'unknown': 'gray'
    }

    # Plot each group with appropriate color
    for (pop, cache_status), group in grouped:
        if pop != 'unknown':
            lat, lon = lookup_location(pop)
            if lat != 0 and lon != 0:  # Skip unknown locations
                color = colors.get(cache_status, 'black')
                marker = 'o' if cache_status == 'HIT' else 'x'
                size = 10 if cache_status == 'HIT' else 8
                ax.plot(lon, lat, marker=marker, color=color, markersize=size, transform=ccrs.Geodetic())

                # Only label each location once
                if not hasattr(plot_all_results, 'labeled') or pop not in plot_all_results.labeled:
                    ax.text(lon + 0.5, lat + 0.5, pop, transform=ccrs.Geodetic(),
                            fontsize=9, fontweight='bold' if cache_status == 'HIT' else 'normal')

                    # Initialize or update labeled set
                    if not hasattr(plot_all_results, 'labeled'):
                        plot_all_results.labeled = set()
                    plot_all_results.labeled.add(pop)

    # Add a legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Cache HIT'),
        Line2D([0], [0], marker='x', color='red', markersize=8, label='Cache MISS'),
        Line2D([0], [0], marker='x', color='orange', markersize=8, label='Cache EXPIRED'),
        Line2D([0], [0], marker='x', color='purple', markersize=8, label='Cache REVALIDATED'),
        Line2D([0], [0], marker='x', color='blue', markersize=8, label='Cache DYNAMIC')
    ]
    ax.legend(handles=legend_elements, loc='lower left')

    plt.title("Discord CDN Cache Status by Location")

    # Save to file
    output_path = "cdn_locations.png"
    plt.savefig(output_path, format='png', dpi=300)
    print(f"[+] Map saved to '{output_path}'")

    # Show plot
    plt.show()


def main():
    start_time = time.time()
    # Validate proxies
    valid_proxies = validate_proxies(PROXIES)
    print(f"[+] {len(valid_proxies)} proxies are valid.\n")

    # Run parallel probing
    print("\n[*] Starting parallel probing...")
    results = probe_parallel(valid_proxies, attempts_per_proxy=5)

    # Process results
    df = pd.DataFrame(results)


    print("\n=== Results Summary ===")
    print(df['Cache'].value_counts().to_string())

    # Show unique PoPs found
    print("\n=== Unique PoPs ===")
    pops = df['PoP'].unique()
    for pop in pops:
        if pop != 'unknown':
            lat, lon = lookup_location(pop)
            print(f"PoP: {pop}, Location: {lat}, {lon}")

    # Display stats
    df_hits = df[df['Cache'] == 'HIT']
    print(f"\n=== Cache HITs: {len(df_hits)} ===\n")
    if not df_hits.empty:
        print(df_hits.to_string(index=False))

        # Create a heatmap of unique victim locations based on cache hits
        print("\n[*] Generating map of all results...")
        plot_all_results(df)
    else:
        print("[-] No cache HITs detected.")

        # Still plot the results even without any HITs
        plot_all_results(df)
    end_time = time.time()
    print(f"[+] Total runtime: {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    main()




#original code
# import requests
# import pandas as pd
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
# import time
# import random
# from concurrent.futures import ThreadPoolExecutor
#
#
# # ==== CONFIG ====
# # Use the exact URL without any query parameters
# CDN_AVATAR_URL = 'https://cdn.discordapp.com/avatars/1368314962623201352/1379ceb959c105e6f137e75b0697ad59.png'
#
# # Add more geographically diverse proxies - these are just examples, replace with working proxies
# # Try to include proxies from different countries/regions for better geographical distribution
# PROXIES = [
#     None,
#     'http://50.223.246.237:80', 'http://50.174.7.159:80', 'http://50.207.199.87:80', 'http://32.223.6.94:80',
#     'http://50.207.199.80:80', 'http://50.207.199.83:80', 'http://50.174.7.153:80', 'http://50.202.75.26:80',
#     'http://50.239.72.18:80', 'http://50.175.212.66:80', 'http://50.217.226.47:80', 'http://50.239.72.16:80',
#     'http://50.239.72.19:80', 'http://50.217.226.40:80', 'http://50.221.74.130:80', 'http://50.175.212.74:80',
#     'http://50.207.199.82:80', 'http://50.174.7.152:80', 'http://50.122.86.118:80', 'http://66.191.31.158:80',
#     'http://89.187.185.88:3128', 'http://23.247.136.254:80', 'http://34.102.48.89:8080', 'http://54.174.151.201:80',
#     'http://40.76.69.94:8080', 'http://155.94.128.59:10809', 'http://50.217.226.43:80', 'http://50.239.72.17:80',
#     'http://50.174.7.157:80', 'http://50.217.226.44:80', 'http://50.174.7.158:80', 'http://50.217.226.42:80',
#     'http://50.174.7.155:80', 'http://50.174.7.162:80', 'http://162.223.90.150:80', 'http://50.221.230.186:80',
#     'http://198.74.51.79:8888', 'http://192.73.244.36:80', 'http://198.49.68.80:80', 'http://50.217.226.41:80',
#     'http://50.207.199.86:80', 'http://68.185.57.66:80', 'http://50.231.104.58:80', 'http://50.174.7.156:80',
#     'http://50.207.199.81:80', 'http://47.252.18.37:6379', 'http://47.252.11.233:8443', 'http://23.82.137.161:80',
#     'http://159.65.245.255:80', 'http://23.247.136.248:80'
#     # Will add more proxies if necessary
# ]
#
# POPS_LAT_LON = {
#     'IAD': (39.0, -77.0),       # Ashburn, VA
#     'ATL': (33.6407, -84.4277), # Atlanta, GA
#     'BOS': (42.3656, -71.0096), # Boston, MA
#     'ORD': (41.9742, -87.9073), # Chicago, IL
#     'DFW': (32.8998, -97.0403), # Dallas, TX
#     'DEN': (39.8561, -104.6737),# Denver, CO
#     'IAH': (29.9902, -95.3368), # Houston, TX
#     'LAS': (36.085, -115.1511), # Las Vegas, NV
#     'LAX': (33.9416, -118.4085),# Los Angeles, CA
#     'MIA': (25.7959, -80.2870), # Miami, FL
#     'MSP': (44.8820, -93.2218), # Minneapolis, MN
#     'JFK': (40.6413, -73.7781), # New York City, NY
#     'EWR': (40.6895, -74.1745), # Newark, NJ
#     'PHX': (33.4342, -112.0116),# Phoenix, AZ
#     'SFO': (37.6213, -122.3790),# San Francisco, CA
#     'SJC': (37.3639, -121.9289),# San Jose, CA
#     'SEA': (47.4502, -122.3088),# Seattle, WA
#     'STL': (38.7487, -90.3700), # St. Louis, MO
#     'TPA': (27.9755, -82.5332), # Tampa, FL
#     'SLC': (40.7899, -111.9791),# Salt Lake City, UT
#     'MCI': (39.2976, -94.7139), # Kansas City, MO
#     'CLE': (41.4117, -81.8498), # Cleveland, OH
#     'PDX': (45.5898, -122.5951),# Portland, OR
#     'CLT': (35.2140, -80.9431), # Charlotte, NC
#     'DTW': (42.2162, -83.3554), # Detroit, MI
#     'PHL': (39.8744, -75.2424), # Philadelphia, PA
#     'BOM': (19.0896, 72.8656),  # Mumbai
#     'MAA': (12.9941, 80.1709),  # Chennai
#     'HYD': (17.2403, 78.4294),  # Hyderabad
#     'DEL': (28.5562, 77.1000),  # New Delhi
#     'CCU': (22.6547, 88.4467),  # Kolkata
#     'BLR': (12.9716, 77.5946),   # Bengaluru
#     'FRA': (50.0379, 8.5622),  # Frankfurt
#     'CDG': (49.0097, 2.5479),  # Paris
#     'LHR': (51.4700, -0.4543),  # London
#     'AMS': (52.3105, 4.7683),  # Amsterdam
#     'NRT': (35.7719, 140.3928),  # Tokyo
#     'SYD': (-33.9399, 151.1753),  # Sydney
#     'GRU': (-23.4356, -46.4731),  # São Paulo
#     'JNB': (-26.1367, 28.2411),  # Johannesburg
#     'SIN': (1.3644, 103.9915),  # Singapore
#     'HKG': (22.3080, 113.9185)  # Hong Kong
# }
#
#
# def lookup_location(p):
#     return POPS_LAT_LON.get(p.upper(), (0, 0))
#
#
# def validate_proxies(proxy_list):
#     working = []
#     print("[*] Validating proxies...")
#
#     for proxy in proxy_list:
#         if proxy is None:
#             working.append(None)
#             print("[+] Local (no proxy) is OK")
#             continue
#         try:
#             r = requests.get("https://www.google.com",
#                              proxies={"http": proxy, "https": proxy},
#                              timeout=5)
#             if r.status_code == 200:
#                 print(f"[+] Proxy works: {proxy}")
#                 working.append(proxy)
#             else:
#                 print(f"[-] Proxy failed (status {r.status_code}): {proxy}")
#         except Exception as e:
#             print(f"[-] Proxy failed ({proxy}): {e}")
#
#     return working
#
#
# def probe_single(proxy=None, attempt=1, session_id=None):
#     """Probe a single proxy with optional session ID to track across attempts"""
#     try:
#         kwargs = {}
#         if proxy:
#             kwargs['proxies'] = {'http': proxy, 'https': proxy}
#
#         # Create headers that will encourage caching
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#             'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Connection': 'keep-alive',
#             # Don't add Cache-Control headers that might prevent caching
#         }
#
#         # Add a session cookie to simulate the same browser across requests
#         if session_id:
#             headers['Cookie'] = f'session={session_id}'
#
#         # CRITICAL: Use the exact same URL without random parameters to increase cache hit chances
#         r = requests.get(CDN_AVATAR_URL, timeout=10, headers=headers, **kwargs)
#
#         ray = r.headers.get('CF-RAY', 'unknown')
#         status = r.headers.get('CF-Cache-Status', 'unknown')
#         pop = ray.split('-')[1] if '-' in ray else 'unknown'
#
#         # Print diagnostics
#         proxy_name = proxy or 'Local'
#         print(f"[Probe {attempt}] {proxy_name} - CF-RAY: {ray}, Cache: {status}, PoP: {pop}")
#
#         # Add more info to the result for better analysis
#         return {
#             'Proxy': proxy_name,
#             'PoP': pop,
#             'Cache': status,
#             'Attempt': attempt,
#             'SessionID': session_id,
#             'CF-RAY': ray
#         }
#     except Exception as e:
#         print(f"[Error] Proxy {proxy} attempt {attempt}: {e}")
#         return None
#
#
# def probe_sequence(proxy, num_attempts=3):
#     """Run a sequence of probes using the same proxy with the same session ID"""
#     session_id = f"session_{random.randint(10000, 99999)}"
#     results = []
#
#     for attempt in range(1, num_attempts + 1):
#         result = probe_single(proxy, attempt, session_id)
#         if result:
#             results.append(result)
#         time.sleep(1)  # Short delay between attempts with the same proxy
#
#     return results
#
#
# def probe_parallel(proxies, attempts_per_proxy=3):
#     """Run probes in parallel for faster execution"""
#     all_results = []
#
#     with ThreadPoolExecutor(max_workers=min(10, len(proxies))) as executor:
#         future_to_proxy = {executor.submit(probe_sequence, proxy, attempts_per_proxy): proxy for proxy in proxies}
#         for future in future_to_proxy:
#             try:
#                 proxy_results = future.result()
#                 all_results.extend(proxy_results)
#             except Exception as e:
#                 print(f"Error in parallel execution: {e}")
#
#     return all_results
#
#
# def plot_all_results(df):
#     """Plot all results including cache hits and misses with different colors"""
#     fig = plt.figure(figsize=(14, 10))
#     ax = plt.axes(projection=ccrs.PlateCarree())
#     ax.coastlines()
#     ax.add_feature(cfeature.BORDERS)
#     ax.add_feature(cfeature.LAND, facecolor='lightgray')
#     ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
#     ax.gridlines(draw_labels=True)
#
#     # Group by PoP and Cache status for plotting
#     grouped = df.groupby(['PoP', 'Cache'])
#
#     # Define colors for different cache statuses
#     colors = {
#         'HIT': 'green',
#         'MISS': 'red',
#         'EXPIRED': 'orange',
#         'REVALIDATED': 'purple',
#         'DYNAMIC': 'blue',
#         'unknown': 'gray'
#     }
#
#     # Plot each group with appropriate color
#     for (pop, cache_status), group in grouped:
#         if pop != 'unknown':
#             lat, lon = lookup_location(pop)
#             if lat != 0 and lon != 0:  # Skip unknown locations
#                 color = colors.get(cache_status, 'black')
#                 marker = 'o' if cache_status == 'HIT' else 'x'
#                 size = 10 if cache_status == 'HIT' else 8
#                 ax.plot(lon, lat, marker=marker, color=color, markersize=size, transform=ccrs.Geodetic())
#
#                 # Only label each location once
#                 if not hasattr(plot_all_results, 'labeled') or pop not in plot_all_results.labeled:
#                     ax.text(lon + 0.5, lat + 0.5, pop, transform=ccrs.Geodetic(),
#                             fontsize=9, fontweight='bold' if cache_status == 'HIT' else 'normal')
#
#                     # Initialize or update labeled set
#                     if not hasattr(plot_all_results, 'labeled'):
#                         plot_all_results.labeled = set()
#                     plot_all_results.labeled.add(pop)
#
#     # Add a legend
#     from matplotlib.lines import Line2D
#     legend_elements = [
#         Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Cache HIT'),
#         Line2D([0], [0], marker='x', color='red', markersize=8, label='Cache MISS'),
#         Line2D([0], [0], marker='x', color='orange', markersize=8, label='Cache EXPIRED'),
#         Line2D([0], [0], marker='x', color='purple', markersize=8, label='Cache REVALIDATED'),
#         Line2D([0], [0], marker='x', color='blue', markersize=8, label='Cache DYNAMIC')
#     ]
#     ax.legend(handles=legend_elements, loc='lower left')
#
#     plt.title("Discord CDN Cache Status by Location")
#
#     # Save to file
#     output_path = "cdn_locations.png"
#     plt.savefig(output_path, format='png', dpi=300)
#     print(f"[+] Map saved to '{output_path}'")
#
#     # Show plot
#     plt.show()
#
#
# def main():
#     # Validate proxies
#     valid_proxies = validate_proxies(PROXIES)
#     print(f"[+] {len(valid_proxies)} proxies are valid.\n")
#
#     # Run parallel probing
#     print("\n[*] Starting parallel probing...")
#     results = probe_parallel(valid_proxies, attempts_per_proxy=5)
#
#     # Process results
#     df = pd.DataFrame(results)
#     print("\n=== Results Summary ===")
#     print(df['Cache'].value_counts().to_string())
#
#     # Show unique PoPs found
#     print("\n=== Unique PoPs ===")
#     pops = df['PoP'].unique()
#     for pop in pops:
#         if pop != 'unknown':
#             lat, lon = lookup_location(pop)
#             print(f"PoP: {pop}, Location: {lat}, {lon}")
#
#     # Display stats
#     df_hits = df[df['Cache'] == 'HIT']
#     print(f"\n=== Cache HITs: {len(df_hits)} ===\n")
#     if not df_hits.empty:
#         print(df_hits.to_string(index=False))
#
#         # Create a heatmap of unique victim locations based on cache hits
#         print("\n[*] Generating map of all results...")
#         plot_all_results(df)
#     else:
#         print("[-] No cache HITs detected.")
#
#         # Still plot the results even without any HITs
#         plot_all_results(df)
#
#
# if __name__ == '__main__':
#     main()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # import requests
# # import pandas as pd
# # import matplotlib.pyplot as plt
# # import cartopy.crs as ccrs
# # import cartopy.feature as cfeature
# # import time
# #
# # # ==== CONFIG ====
# # # Fixed URL format
# # CDN_AVATAR_URL = 'https://cdn.discordapp.com/avatars/1368314962623201352/1379ceb959c105e6f137e75b0697ad59.png'
# #
# # # Add query parameter for different sizes to potentially trigger different cache behavior
# # # CDN_AVATAR_URL = 'https://cdn.discordapp.com/avatars/1368314962623201352/1379ceb959c105e6f137e75b0697ad59.png?size=1024'
# #
# # PROXIES = [
# #     None,
# #     'http://50.223.246.237:80', 'http://50.174.7.159:80', 'http://50.207.199.87:80', 'http://32.223.6.94:80',
# #     'http://50.207.199.80:80', 'http://50.207.199.83:80', 'http://50.174.7.153:80', 'http://50.202.75.26:80',
# #     'http://50.239.72.18:80', 'http://50.175.212.66:80', 'http://50.217.226.47:80', 'http://50.239.72.16:80',
# #     'http://50.239.72.19:80', 'http://50.217.226.40:80', 'http://50.221.74.130:80', 'http://50.175.212.74:80',
# #     'http://50.207.199.82:80', 'http://50.174.7.152:80', 'http://50.122.86.118:80', 'http://66.191.31.158:80',
# #     'http://89.187.185.88:3128', 'http://23.247.136.254:80', 'http://34.102.48.89:8080', 'http://54.174.151.201:80',
# #     'http://40.76.69.94:8080', 'http://155.94.128.59:10809', 'http://50.217.226.43:80', 'http://50.239.72.17:80',
# #     'http://50.174.7.157:80', 'http://50.217.226.44:80', 'http://50.174.7.158:80', 'http://50.217.226.42:80',
# #     'http://50.174.7.155:80', 'http://50.174.7.162:80', 'http://162.223.90.150:80', 'http://50.221.230.186:80',
# #     'http://198.74.51.79:8888', 'http://192.73.244.36:80', 'http://198.49.68.80:80', 'http://50.217.226.41:80',
# #     'http://50.207.199.86:80', 'http://68.185.57.66:80', 'http://50.231.104.58:80', 'http://50.174.7.156:80',
# #     'http://50.207.199.81:80', 'http://47.252.18.37:6379', 'http://47.252.11.233:8443', 'http://23.82.137.161:80',
# #     'http://159.65.245.255:80', 'http://23.247.136.248:80'
# # ]
# #
# # POPS_LAT_LON = {
# #     'IAD': (39.0, -77.0), 'ATL': (33.6407, -84.4277), 'BOS': (42.3656, -71.0096), 'ORD': (41.9742, -87.9073),
# #     'DFW': (32.8998, -97.0403), 'DEN': (39.8561, -104.6737), 'IAH': (29.9902, -95.3368), 'LAS': (36.085, -115.1511),
# #     'LAX': (33.9416, -118.4085), 'MIA': (25.7959, -80.2870), 'MSP': (44.8820, -93.2218), 'JFK': (40.6413, -73.7781),
# #     'EWR': (40.6895, -74.1745), 'PHX': (33.4342, -112.0116), 'SFO': (37.6213, -122.3790), 'SJC': (37.3639, -121.9289),
# #     'SEA': (47.4502, -122.3088), 'STL': (38.7487, -90.3700), 'TPA': (27.9755, -82.5332), 'SLC': (40.7899, -111.9791),
# #     'MCI': (39.2976, -94.7139), 'CLE': (41.4117, -81.8498), 'PDX': (45.5898, -122.5951), 'CLT': (35.2140, -80.9431),
# #     'DTW': (42.2162, -83.3554), 'PHL': (39.8744, -75.2424), 'BOM': (19.0896, 72.8656), 'MAA': (12.9941, 80.1709),
# #     'HYD': (17.2403, 78.4294), 'DEL': (28.5562, 77.1000), 'CCU': (22.6547, 88.4467), 'BLR': (12.9716, 77.5946)
# # }
# #
# #
# # def lookup_location(p):
# #     return POPS_LAT_LON.get(p.upper(), (0, 0))
# #
# #
# # def validate_proxies(proxy_list):
# #     working = []
# #     print("[*] Validating proxies...")
# #     for proxy in proxy_list:
# #         if proxy is None:
# #             working.append(None)
# #             print("[+] Local (no proxy) is OK")
# #             continue
# #         try:
# #             r = requests.get("https://www.google.com", proxies={"http": proxy, "https": proxy}, timeout=5)
# #             if r.status_code == 200:
# #                 print(f"[+] Proxy works: {proxy}")
# #                 working.append(proxy)
# #             else:
# #                 print(f"[-] Proxy failed (status {r.status_code}): {proxy}")
# #         except Exception as e:
# #             print(f"[-] Proxy failed ({proxy}): {e}")
# #     return working
# #
# #
# # def probe(proxy=None):
# #     try:
# #         kwargs = {}
# #         if proxy:
# #             kwargs['proxies'] = {'http': proxy, 'https': proxy}
# #
# #         # Add randomized query parameter to avoid query caching
# #         import random
# #         random_param = f"?nocache={random.randint(1, 1000000)}"
# #         url = CDN_AVATAR_URL + random_param
# #
# #         # Modified request with specific headers to improve cache hit chances
# #         headers = {
# #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
# #             'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
# #             'Accept-Encoding': 'gzip, deflate, br',
# #             'Connection': 'keep-alive',
# #             'Cache-Control': 'max-age=0'  # This might help with getting cache hits
# #         }
# #
# #         r = requests.get(url, timeout=10, headers=headers, **kwargs)
# #         ray = r.headers.get('CF-RAY', 'unknown')
# #         status = r.headers.get('CF-Cache-Status', 'unknown')
# #         pop = ray.split('-')[1] if '-' in ray else 'unknown'
# #
# #         # Print all headers for debugging
# #         print(f"[Probe] {proxy or 'Local'} - CF-RAY: {ray}, Cache: {status}, PoP: {pop}")
# #         print(f"[Headers] {dict(r.headers)}")
# #
# #         return {'Proxy': proxy or 'Local', 'PoP': pop, 'Cache': status}
# #     except Exception as e:
# #         print(f"[Error] Proxy {proxy}: {e}")
# #         return None
# #
# #
# # def plot_hits(df):
# #     fig = plt.figure(figsize=(14, 8))
# #     ax = plt.axes(projection=ccrs.PlateCarree())
# #     ax.coastlines()
# #     ax.add_feature(cfeature.BORDERS)
# #     ax.add_feature(cfeature.LAND)
# #     ax.add_feature(cfeature.OCEAN)
# #     ax.gridlines(draw_labels=True)
# #
# #     for _, row in df.iterrows():
# #         lat, lon = lookup_location(row['PoP'])
# #         ax.plot(lon, lat, 'ro', markersize=6, transform=ccrs.Geodetic())
# #         ax.text(lon + 0.5, lat + 0.5, row['PoP'], transform=ccrs.Geodetic())
# #
# #     plt.title("CDN Cache HIT Locations")
# #
# #     # Save to file
# #     output_path = "cdn_heatmap.jpg"
# #     plt.savefig(output_path, format='jpeg', dpi=300)
# #     print(f"[+] Heatmap saved to '{output_path}'")
# #
# #     # Show plot
# #     plt.show()
# #
# #
# # def main():
# #     # Just use a small subset of proxies for testing
# #     test_proxies = PROXIES[:10]  # Only test first 10 proxies
# #
# #     valid_proxies = validate_proxies(test_proxies)
# #     print(f"[+] {len(valid_proxies)} proxies are valid.\n")
# #
# #     # Try multiple rounds of probing to increase chance of cache hits
# #     all_results = []
# #
# #     for round in range(3):  # Try 3 rounds of probing
# #         print(f"\n=== Round {round + 1} of probing ===")
# #         results = []
# #         for proxy in valid_proxies:
# #             res = probe(proxy)
# #             if res:
# #                 results.append(res)
# #             time.sleep(2)  # Add delay between requests
# #
# #         all_results.extend(results)
# #
# #         # Check if we got any hits in this round
# #         df = pd.DataFrame(results)
# #         hits = df[df['Cache'] == 'HIT']
# #         if not hits.empty:
# #             print(f"[+] Found {len(hits)} cache hits in round {round + 1}!")
# #         else:
# #             print(f"[-] No cache hits in round {round + 1}")
# #
# #         # Wait a bit longer between rounds
# #         if round < 2:  # Don't wait after the last round
# #             print("Waiting 10 seconds before next round...")
# #             time.sleep(10)
# #
# #     # Process all results
# #     df_all = pd.DataFrame(all_results)
# #     df_hits = df_all[df_all['Cache'] == 'HIT']
# #
# #     print("\n=== Cache HITs ===\n", df_hits)
# #
# #     # Also show MISSes for debugging
# #     df_misses = df_all[df_all['Cache'] == 'MISS']
# #     print("\n=== Cache MISSes ===\n", df_misses.head())  # Just show first few misses
# #
# #     if not df_hits.empty:
# #         plot_hits(df_hits)
# #     else:
# #         print("[-] No CDN cache HITs detected across all rounds.")
# #
# #
# # if __name__ == '__main__':
# #     main()
# # # import requests
# # # import pandas as pd
# # # import matplotlib.pyplot as plt
# # # import cartopy.crs as ccrs
# # # import cartopy.feature as cfeature
# # # import time
# # #
# # # # ==== CONFIG ====
# # # CDN_AVATAR_URL = 'https://cdn.discordapp.com/avatars/1368314962623201352/https://cdn.discordapp.com/avatars/1368314962623201352/1379ceb959c105e6f137e75b0697ad59.png?size=1024.png'
# # #
# # # PROXIES = [
# # #     None,
# # #     'http://50.223.246.237:80', 'http://50.174.7.159:80', 'http://50.207.199.87:80', 'http://32.223.6.94:80',
# # #     'http://50.207.199.80:80', 'http://50.207.199.83:80', 'http://50.174.7.153:80', 'http://50.202.75.26:80',
# # #     'http://50.239.72.18:80', 'http://50.175.212.66:80', 'http://50.217.226.47:80', 'http://50.239.72.16:80',
# # #     'http://50.239.72.19:80', 'http://50.217.226.40:80', 'http://50.221.74.130:80', 'http://50.175.212.74:80',
# # #     'http://50.207.199.82:80', 'http://50.174.7.152:80', 'http://50.122.86.118:80', 'http://66.191.31.158:80',
# # #     'http://89.187.185.88:3128', 'http://23.247.136.254:80', 'http://34.102.48.89:8080', 'http://54.174.151.201:80',
# # #     'http://40.76.69.94:8080', 'http://155.94.128.59:10809', 'http://50.217.226.43:80', 'http://50.239.72.17:80',
# # #     'http://50.174.7.157:80', 'http://50.217.226.44:80', 'http://50.174.7.158:80', 'http://50.217.226.42:80',
# # #     'http://50.174.7.155:80', 'http://50.174.7.162:80', 'http://162.223.90.150:80', 'http://50.221.230.186:80',
# # #     'http://198.74.51.79:8888', 'http://192.73.244.36:80', 'http://198.49.68.80:80', 'http://50.217.226.41:80',
# # #     'http://50.207.199.86:80', 'http://68.185.57.66:80', 'http://50.231.104.58:80', 'http://50.174.7.156:80',
# # #     'http://50.207.199.81:80', 'http://47.252.18.37:6379', 'http://47.252.11.233:8443', 'http://23.82.137.161:80',
# # #     'http://159.65.245.255:80', 'http://23.247.136.248:80'
# # # ]
# # #
# # # POPS_LAT_LON = {
# # #     'IAD': (39.0, -77.0), 'ATL': (33.6407, -84.4277), 'BOS': (42.3656, -71.0096), 'ORD': (41.9742, -87.9073),
# # #     'DFW': (32.8998, -97.0403), 'DEN': (39.8561, -104.6737), 'IAH': (29.9902, -95.3368), 'LAS': (36.085, -115.1511),
# # #     'LAX': (33.9416, -118.4085), 'MIA': (25.7959, -80.2870), 'MSP': (44.8820, -93.2218), 'JFK': (40.6413, -73.7781),
# # #     'EWR': (40.6895, -74.1745), 'PHX': (33.4342, -112.0116), 'SFO': (37.6213, -122.3790), 'SJC': (37.3639, -121.9289),
# # #     'SEA': (47.4502, -122.3088), 'STL': (38.7487, -90.3700), 'TPA': (27.9755, -82.5332), 'SLC': (40.7899, -111.9791),
# # #     'MCI': (39.2976, -94.7139), 'CLE': (41.4117, -81.8498), 'PDX': (45.5898, -122.5951), 'CLT': (35.2140, -80.9431),
# # #     'DTW': (42.2162, -83.3554), 'PHL': (39.8744, -75.2424), 'BOM': (19.0896, 72.8656), 'MAA': (12.9941, 80.1709),
# # #     'HYD': (17.2403, 78.4294), 'DEL': (28.5562, 77.1000), 'CCU': (22.6547, 88.4467), 'BLR': (12.9716, 77.5946)
# # # }
# # #
# # # def lookup_location(p):
# # #     return POPS_LAT_LON.get(p.upper(), (0, 0))
# # #
# # # def validate_proxies(proxy_list):
# # #     working = []
# # #     print("[*] Validating proxies...")
# # #     for proxy in proxy_list:
# # #         if proxy is None:
# # #             working.append(None)
# # #             print("[+] Local (no proxy) is OK")
# # #             continue
# # #         try:
# # #             r = requests.get("https://www.google.com", proxies={"http": proxy, "https": proxy}, timeout=5)
# # #             if r.status_code == 200:
# # #                 print(f"[+] Proxy works: {proxy}")
# # #                 working.append(proxy)
# # #             else:
# # #                 print(f"[-] Proxy failed (status {r.status_code}): {proxy}")
# # #         except Exception as e:
# # #             print(f"[-] Proxy failed ({proxy}): {e}")
# # #     return working
# # #
# # # def probe(proxy=None):
# # #     try:
# # #         kwargs = {}
# # #         if proxy:
# # #             kwargs['proxies'] = {'http': proxy, 'https': proxy}
# # #         r = requests.get(CDN_AVATAR_URL, timeout=10, headers={'User-Agent': 'Mozilla/5.0'}, **kwargs)
# # #         ray = r.headers.get('CF-RAY', 'unknown')
# # #         status = r.headers.get('CF-Cache-Status', 'unknown')
# # #         pop = ray.split('-')[1] if '-' in ray else 'unknown'
# # #         print(f"[Probe] {proxy or 'Local'} - CF-RAY: {ray}, Cache: {status}, PoP: {pop}")
# # #         return {'Proxy': proxy or 'Local', 'PoP': pop, 'Cache': status}
# # #     except Exception as e:
# # #         print(f"[Error] Proxy {proxy}: {e}")
# # #         return None
# # #
# # # def plot_hits(df):
# # #     fig = plt.figure(figsize=(14, 8))
# # #     ax = plt.axes(projection=ccrs.PlateCarree())
# # #     ax.coastlines()
# # #     ax.add_feature(cfeature.BORDERS)
# # #     ax.add_feature(cfeature.LAND)
# # #     ax.add_feature(cfeature.OCEAN)
# # #     ax.gridlines(draw_labels=True)
# # #
# # #     for _, row in df.iterrows():
# # #         lat, lon = lookup_location(row['PoP'])
# # #         ax.plot(lon, lat, 'ro', markersize=6, transform=ccrs.Geodetic())
# # #         ax.text(lon + 0.5, lat + 0.5, row['PoP'], transform=ccrs.Geodetic())
# # #
# # #     plt.title("CDN Cache HIT Locations")
# # #
# # #     # Save to file
# # #     output_path = "cdn_heatmap.jpg"
# # #     plt.savefig(output_path, format='jpeg', dpi=300)
# # #     print(f"[+] Heatmap saved to '{output_path}'")
# # #
# # #     # Show plot
# # #     plt.show()
# # #
# # #
# # # def main():
# # #     valid_proxies = validate_proxies(PROXIES)
# # #     print(f"[+] {len(valid_proxies)} proxies are valid.\n")
# # #     results = []
# # #     for proxy in valid_proxies:
# # #         res = probe(proxy)
# # #         if res:
# # #             results.append(res)
# # #         time.sleep(2)
# # #
# # #     df = pd.DataFrame(results)
# # #     df_hits = df[df['Cache'] == 'HIT']
# # #     print("\n=== Cache HITs ===\n", df_hits)
# # #
# # #     if not df_hits.empty:
# # #         plot_hits(df_hits)
# # #     else:
# # #         print("[-] No CDN cache HITs detected.")
# # #
# # # if __name__ == '__main__':
# # #     main()
