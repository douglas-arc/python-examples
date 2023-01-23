import requests, gzip, itertools
from sys import argv
from collections import Counter

def top_packages(architecture, mirror_path = 'http://ftp.uk.debian.org/debian/dists/stable/main/'):
    
    architecture = architecture.lower()
    contents_file = ''.join([mirror_path, 'Contents-', architecture, '.gz'])

    downloaded_file = requests.get(contents_file)
    decompressed_file = gzip.decompress(downloaded_file.content).decode('utf-8').split()
    
    packages_column = decompressed_file[1::2]
    all_packages = []

    # Case where more than one package is associated with a filename
    for item in packages_column:
        all_packages.append(item.split(','))

    # Flattens the all_packages list before counting
    all_packages = list(itertools.chain(*all_packages))
    counted_packages = Counter(all_packages)
    top_10_packages = counted_packages.most_common()[:10]

    print()
    message = '{rank}. {package_name} {number_of_files}'

    for i, package in enumerate(top_10_packages):
        print(message.format(rank = i+1, package_name = package[0], number_of_files = package[1]))


if len(argv) == 2: 
    top_packages(argv[1])
elif len(argv) == 3: 
    top_packages(argv[1], argv[2])
else:
    raise ValueError("Invalid arguments. USAGE: ./package_statistics.py <architecture> [mirror_path]")
